import io
import csv
import logging

from django.conf import settings
from django.db import DatabaseError
from django.db.models import ForeignKey
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from callingcards.callingcards.tasks import (process_upload,
                                             upload_csv_postgres_task)

logger = logging.getLogger(__name__)


class CustomCreateMixin:
    """
    By default the user field is "user" you can change it
    to your model "user" field.
    cite: https://xploit29.com/2016/09/15/django-rest-framework-auto-assign-current-user-on-creation/

    Usage:
    class PostViewSet(CustomCreateMixin, PageSizeModelMixin,
                      viewsets.ModelViewSet, CountModelMixin):
        # ViewsSet required info...
        user_field = 'creator'
    """

    _user_field = None
    _modifiedby_field = None

    @property
    def user_field(self):
        """user field is the field from the model that will be
          set to the current user. defaults to "uploader" """
        return self._user_field or 'uploader'

    @user_field.setter
    def user_field(self, value):
        self._user_field = value

    @property
    def modifiedby_field(self):
        """modifiedby field is the field from the model that will be
          set to the current user. defaults to "modifiedby" """
        return self._modifiedby_field or 'modifiedBy'

    @modifiedby_field.setter
    def modifiedby_field(self, value):
        self._modifiedby_field = value

    def get_foreign_key_fields(self, pop_user_field=True):
        """
        Get a dictionary of foreign key fields for the model associated with
        the queryset. The dictionary keys are the field names and the values
        are the related models.

        Args:
            pop_user_field (bool): If True (default), exclude the field
            specified in the user_field property from the returned dictionary.

        Returns:
            dict: A dictionary containing the foreign key fields and 
            their related models.
        """
        foreign_key_fields = {
            field.name: field.related_model
            for field in self.queryset.model._meta.get_fields()
            if isinstance(field, ForeignKey)
        }

        if pop_user_field:
            foreign_key_fields.pop(self.user_field, None)

        return foreign_key_fields

    def create(self, request, *args, **kwargs):
        """ overwrite default create to accept either single or multiple
        records on create/update
            cite: https://stackoverflow.com/a/65078963/9708266
            accept either an array or a single object,
            eg {"field1": "", "field2": "", ...} or
            [{"field1": "", "field2": "", ...},
            {"field1": "", "field2": "", ...}, ...]
        """
        many_flag = True if isinstance(request.data, list) else False

        kwargs = {
            self.user_field: self.request.user,
            self.modifiedby_field: self.request.user
        }

        serializer = self.get_serializer(data=request.data, many=many_flag)
        serializer.is_valid(raise_exception=True)
        serializer.save(**kwargs)

        if many_flag:
            headers = None
        else:
            headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    @action(detail=False, methods=['post'], url_path='create-async')
    def create_async(self, request, *args, **kwargs):
        """ Asynchronously create records"""
        many_flag = True if isinstance(request.data, list) else False
        kwargs = {
            self.user_field: self.request.user.pk,
            'serializer_class_path': f'{self.serializer_class.__module__}'
                                     f'.{self.serializer_class.__name__}'
        }

        # Call the Celery task with the request data and user_field
        result = process_upload.delay(request.data, many_flag, kwargs)

        return Response({"status":
                         f"Upload in progress. Task ID: {result.task_id}"})

    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request, *args, **kwargs):
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            return Response({"error": "No CSV file provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Read the input CSV file and add the user_uuid to each row
        file_data = csv_file.read().decode('utf-8')
        input_data = io.StringIO(file_data)

        # Process the header row and add the additional columns
        header = next(csv.reader(input_data))

        # get a list of the foriegn key fields in the model
        foreign_key_fields = self.get_foreign_key_fields()

        # Process the remaining rows and add the additional columns to each row
        # user_uuid = str(request.user.id)
        rows = []
        for row in csv.reader(input_data):
            # Combine the header and row using zip and create a dictionary
            row_dict = {header[i]: row[i] for i in range(len(header))}

            # Handle foreign key fields
            for field, related_model in foreign_key_fields.items():
                if field in row_dict:
                    try:
                        related_id = int(row_dict[field])
                        row_dict[field] = \
                            related_model.objects.get(id=related_id)
                    except (related_model.DoesNotExist, ValueError, TypeError):
                        return Response({"error": f"Invalid '{field}' "
                                         f"value '{row_dict[field]}'"
                                         f"on line {csv.reader.line_num}"},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Add the additional fields to the dictionary
            row_dict[self.user_field] = self.request.user
            row_dict[self.modifiedby_field] = self.request.user
            rows.append(row_dict)

        # Bulk create the rows in the database
        try:
            objs = [self.queryset.model(**row_dict) for row_dict in rows]
            self.queryset.model.objects.bulk_create(objs)
        except (DatabaseError, ValueError) as err:
            # Extract the relevant information from the error
            error_message = str(err)
            logger.debug(error_message)
            lines_with_errors = set()
            for line in error_message.split("\n"):
                if "INSERT INTO" in line:
                    line_parts = line.split(" ")
                    line_number = int(line_parts[3].replace("(", ""))
                    lines_with_errors.add(line_number)

            # Construct the error response message
            if len(lines_with_errors) == 1:
                error_msg = f"Error during CSV upload: {error_message}"
            else:
                error_msg = ("Errors during CSV upload on lines: "
                             f"{', '.join(map(str, sorted(lines_with_errors)))}")  # noqa

            return Response({"error": error_msg},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "CSV data uploaded successfully."},
                        status=status.HTTP_201_CREATED)

    # this is postgresql specific. May be faster, but lose the db agnostic
    # nature of the django API
    @action(detail=False, methods=['post'], url_path='upload-csv-postgres')
    def upload_csv_postgres(self, request, *args, **kwargs):

        # Check if the database engine is PostgreSQL
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' not in db_engine:
            return Response({"error":
                             "CSV upload is only supported "
                             "for PostgreSQL database engine."},
                            status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            return Response({"error": "No CSV file provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # get a list of the foriegn key fields in the model
        foreign_key_fields = self.get_foreign_key_fields()

        table_name = self.queryset.model._meta.db_table

        # Process the remaining rows and add the additional columns to each row
        user_uuid = str(request.user.id)

        # Read the input CSV file and add the user_uuid to each row
        file_data = csv_file.read().decode('utf-8')
        upload_csv_postgres_task.delay(file_data,
                                       user_uuid,
                                       table_name,
                                       foreign_key_fields)

        return Response({"status": "CSV data upload initiated."})
