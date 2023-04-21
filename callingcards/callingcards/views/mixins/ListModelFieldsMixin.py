from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class ListModelFieldsMixin:
    @action(detail=False, methods=['get'])
    def fields(self, request, *args, **kwargs):

        # Get the _readable_fields attribute of the dummy serializer instance
        readable = [field.source for field in
                    self.get_serializer()._readable_fields]
        writable = [field.source for field in
                    self.get_serializer()._writable_fields]
        automatically_generated = ['id',
                                   'uploader',
                                   'uploadDate',
                                   'modified']

        filter_fields = kwargs.get('filter_fields', None)
        if not filter_fields:
            try:
                filter_fields = self.filterset_class.Meta.fields
            except AttributeError:
                # Use the custom_filter_columns attribute if available
                # this needs to be set in the viewset class when there is no
                # filterset_class
                filter_fields = getattr(self, 'custom_filter_columns', None)

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_fields},
                        status=status.HTTP_200_OK)
