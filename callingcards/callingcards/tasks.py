import logging
from typing import TYPE_CHECKING
import csv
import io
import os
import gzip
import datetime
from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import connection, DatabaseError
from django.utils.timezone import now
from psycopg2 import errors
from celery import shared_task

from ..users.models import User
from ..celery import app
from .models import (CallingCardsSig,
                     CCExperiment, HopsSource,
                     BackgroundSource,
                     PromoterRegionsSource)
from .utils.callingcards_with_metrics import callingcards_with_metrics

logger = logging.getLogger(__name__)


@app.task
def process_upload(data, many_flag, kwargs):
    """
    Function to upload records using a serializer with a request.user
    to determine the uploader field value.
    """
    serializer_class_path = kwargs.pop("serializer_class_path")
    serializer_class = import_string(serializer_class_path)

    user_pk = kwargs.pop("uploader")
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    # TODO document that the user_field and modifiedBy_field may be passed
    # in the kwargs
    kwargs[kwargs.get('user_field', 'uploader')] = user
    kwargs[kwargs.get('modifiedBy_field', 'modifiedBy')] = user

    if many_flag:
        serializer = serializer_class(data=data, many=True)
    else:
        serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(**kwargs)
    return serializer.data


@shared_task
def upload_csv_postgres_task(file_data,
                             user_uuid,
                             table_name,
                             foreign_key_fields):
    # Read the input CSV file and add the user_uuid to each row
    input_data = io.StringIO(file_data)

    # Create a new StringIO object to store the modified data
    data_file = io.StringIO()
    reader = csv.reader(input_data)
    writer = csv.writer(data_file)

    # Process the header row and add the additional columns
    header = next(reader)

    # Check for foreign key fields and add "_id" to them
    header = [field + '_id' if field in foreign_key_fields
              else field for field in header]

    # TODO remove hard coding on these fields
    # append the django managed fields
    header.append('uploader_id')
    header.append('uploadDate')
    header.append('modifiedBy_id')
    header.append('modified')
    writer.writerow(header)

    # Process the remaining rows and add the additional columns to each row
    for row in reader:
        row.append(user_uuid)
        # Add the current date for uploadDate
        row.append(now().date())
        # add the user_uuid for modifiedBy
        row.append(user_uuid)
        # Add the current datetime for modified
        row.append(now())
        writer.writerow(row)

    # Reset the data_file cursor to the beginning
    data_file.seek(0)

    # Connect to the database using Django's connection
    conn = connection
    conn.ensure_connection()

    with conn.connection as db_conn:
        try:
            # Load the data using the COPY command
            cursor = db_conn.cursor()

            # Read the header line to get the column names
            header_line = data_file.readline().strip()
            columns = [f'"{col}"' for col in csv.reader([header_line]).__next__()]  # noqa

            copy_command = f"COPY {table_name} ({', '.join(columns)}) FROM STDIN WITH CSV HEADER"  # noqa
            cursor.copy_expert(copy_command, data_file)

            db_conn.commit()

        except (errors.UniqueViolation, errors.ForeignKeyViolation) as err:
            db_conn.rollback()
            error_message = f"Error during CSV upload: {err}"
            if hasattr(err, 'lineno'):
                error_message += f" at line {err.lineno}"
            raise Exception(error_message)

        except DatabaseError as err:
            db_conn.rollback()
            raise Exception(f"Error during CSV upload: {err}")


@shared_task
def process_experiment(experiment_id: int, user_id: int, **kwargs):

    user = User.objects.get(pk=user_id)

    try:
        result_df = callingcards_with_metrics(
            {'experiment_id': experiment_id,
             'hops_source': kwargs.get('hops_source', None),
             'background_source': kwargs.get('background_source', None),
             'promoter_source': kwargs.get('promoter_source', None)})
    except ValueError as err:
        # log the info and continue on to the next item in
        # the experiment_id_list
        raise ValueError(f'callingcards_with_metrics failed on '
                         f'experiment_id: {str(experiment_id)} '
                         f'with kwargs: {kwargs}') from err
    # cache the result in the database
    grouped = result_df.groupby(['experiment_id',
                                 'hops_source',
                                 'background_source',
                                 'promoter_source'])
    for name, group in grouped:
        logger.debug('processing group: %s', name)
        (experiment_id_tmp, hops_source,
            background_source, promoter_source) = name

        # Compress the dataframe and write it to the buffer
        compressed_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_buffer,
                           mode='wb') as gz:
            group.to_csv(gz, index=False, encoding='utf-8')

        # Reset the buffer's position to the beginning
        compressed_buffer.seek(0)

        # Save the file to Django's default storage
        filepath = os.path.join(
            'analysis',
            CCExperiment.objects.get(pk=experiment_id).batch,
            f'ccexperiment_{experiment_id}',
            f'{hops_source}'
            f'_{background_source}'
            f'_{promoter_source}.csv.gz')

        logger.debug("filepath: %s", filepath)

        default_storage.save(
            filepath,
            ContentFile(compressed_buffer.read()))

        # Close the buffer
        compressed_buffer.close()

        CallingCardsSig.objects.create(
            uploader=user,
            uploadDate=datetime.date.today(),
            modified=datetime.datetime.now(),
            modifiedBy=user,
            experiment=CCExperiment.objects.get(pk=experiment_id),
            hops_source=HopsSource.objects.get(pk=hops_source),
            background_source=BackgroundSource.objects.get(
                pk=background_source),
            promoter_source=PromoterRegionsSource.objects.get(
                pk=promoter_source),
            file=filepath)