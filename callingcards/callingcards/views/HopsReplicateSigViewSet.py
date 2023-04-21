from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import HopsReplicateSig
from ..serializers import (HopsReplicateSigSerializer,
                           HopsReplicateSigAnnotatedSerializer)
from ..filters import HopsReplicateSigFilter


class HopsReplicateSigViewSet(ListModelFieldsMixin,
                              CustomCreateMixin,
                              CustomValidateMixin,
                              UpdateModifiedMixin,
                              PageSizeModelMixin,
                              viewsets.ModelViewSet,
                              CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HopsReplicateSig.objects.all().order_by('id')  # noqa
    serializer_class = HopsReplicateSigSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = HopsReplicateSigFilter

    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['promoterregions__associated_features__locus_tag',
                     'promoterregions___associated_features__gene',
                     'experiment__tf__tf__locus_tag',
                     'experiment___tf__tf__gene']

    @action(detail=False, methods=['get'], url_path='with_annote',
            url_name='with-annote')
    def with_annotations(self, request, *args, **kwargs):
        annotated_queryset = HopsReplicateSig.objects\
            .with_annotations().order_by('id')

        # Apply the filtering
        filtered_queryset = self.filter_queryset(annotated_queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = HopsReplicateSigAnnotatedSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HopsReplicateSigAnnotatedSerializer(filtered_queryset,
                                                         many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='with_annote/count',
            url_name='with-annote-count')
    def with_annotations_count(self, request, *args, **kwargs) -> Response:
        hops_with_annotations = HopsReplicateSig\
            .objects.with_annotations()
        hops_with_annotations_fltr = HopsReplicateSigFilter(
            self.request.GET,
            queryset=hops_with_annotations)
        content = {'count': self.get_count(hops_with_annotations_fltr.qs)}
        return Response(content)

    @action(detail=False, url_path='with_annote/pagination_info',
            url_name='with-annote-pagination-info')
    def with_annotations_pagination_info(self, request,
                                         *args, **kwargs) -> Response:
        return self.pagination_info(request, *args, **kwargs)

    @action(detail=False, url_path='with_annote/fields',
            url_name='with-annote-fields')
    def with_annotations_fields(self, request, *args, **kwargs) -> Response:
        # Use GeneWithEffectsSerializer instead of DummySerializer
        readable = [field.source for field in
                    HopsReplicateSigAnnotatedSerializer()._readable_fields]
        writable = None
        automatically_generated = ['id',
                                   'uploader',
                                   'uploadDate',
                                   'modified']

        filter_columns = HopsReplicateSigFilter.Meta.fields

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                        "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_columns},
                        status=status.HTTP_200_OK)
