from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import HarbisonChIP
from ..serializers import (HarbisonChIPSerializer,
                           HarbisonChIPAnnotatedSerializer)
from ..filters import HarbisonChIPFilter

class HarbisonChIPViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          CustomValidateMixin,
                          UpdateModifiedMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HarbisonChIP.objects.all().order_by('id')  # noqa
    serializer_class = HarbisonChIPSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = HarbisonChIPFilter

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['associated_feature__locus_tag',
                     'associated_feature__gene', 'source']

    @action(detail=False, methods=['get'], url_path='with_annote',
            url_name='with-annote')
    def with_annotations(self, request, *args, **kwargs):
        annotated_queryset = HarbisonChIP.objects\
            .with_annotations().order_by('id')

        # Apply the filtering
        filtered_queryset = self.filter_queryset(annotated_queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = HarbisonChIPAnnotatedSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HarbisonChIPAnnotatedSerializer(
            filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='with_annote/count',
            url_name='with-annote-count')
    def with_annotations_count(self, request, *args, **kwargs) -> Response:
        annote_qs = HarbisonChIP.objects.with_annotations()
        annote_qs_fltr = HarbisonChIPFilter(
            self.request.GET,
            queryset=annote_qs)
        content = {'count': self.get_count(annote_qs_fltr.qs)}
        return Response(content)

    @action(detail=False, url_path='with_annote/pagination_info',
            url_name='with-annote-pagination-info')
    def with_annotations_pagination_info(self, request,
                                         *args, **kwargs) -> Response:
        return self.pagination_info(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='with_annote/fields',
            url_name='with-annote-fields')
    def with_annotation_fields(self, request, *args, **kwargs):
        # Get the _readable_fields attribute of the
        # HarbisonChIPAnnotatedSerializer instance
        readable = [field.source for field in
                    HarbisonChIPAnnotatedSerializer()._readable_fields]
        writable = None
        automatically_generated = None
        filter_columns = HarbisonChIPFilter.Meta.fields

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_columns},
                        status=status.HTTP_200_OK)
