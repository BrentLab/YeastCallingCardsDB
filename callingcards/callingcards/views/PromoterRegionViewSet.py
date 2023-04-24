import logging
from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

import pandas as pd

from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import PromoterRegions
from ..serializers import (PromoterRegionsSerializer,
                           PromoterRegionsTargetsOnlySerializer)
from ..filters import PromoterRegionsFilter
from ..utils.callingcards_with_metrics import callingcards_with_metrics

logger = logging.getLogger(__name__)


class PromoterRegionsViewSet(ListModelFieldsMixin,
                             CustomCreateMixin,
                             CustomValidateMixin,
                             UpdateModifiedMixin,
                             PageSizeModelMixin,
                             viewsets.ModelViewSet,
                             CountModelMixin):
    queryset = PromoterRegions.objects.all().order_by('id')  # noqa
    serializer_class = PromoterRegionsSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = PromoterRegionsFilter

    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['associated_feature__locus_tag',
                     'associated_feature__gene', 'source']

    @action(detail=False, methods=['get'], url_path='targets',
            url_name='targets')
    def targets(self, request, *args, **kwargs):
        targets_queryset = PromoterRegions.objects\
            .targets()\
            .order_by('id')

        # Apply the filtering
        filtered_queryset = self.filter_queryset(targets_queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = PromoterRegionsTargetsOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PromoterRegionsTargetsOnlySerializer(filtered_queryset,
                                                          many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='targets/count',
            url_name='targets-count')
    def targets_count(self, request, *args, **kwargs) -> Response:
        annote_qs = PromoterRegions.objects.targets()
        annote_qs_fltr = PromoterRegionsFilter(
            self.request.GET,
            queryset=annote_qs)
        content = {'count': self.get_count(annote_qs_fltr.qs)}
        return Response(content)

    @action(detail=False, url_path='targets/pagination_info',
            url_name='targets-pagination-info')
    def targets_pagination_info(self, request,
                                *args, **kwargs) -> Response:
        return self.pagination_info(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='targets/fields',
            url_name='targets-fields')
    def targets_fields(self, request, *args, **kwargs):
        readable = [field.source for field in
                    PromoterRegionsTargetsOnlySerializer()._readable_fields]
        writable = None
        automatically_generated = None
        filter_columns = PromoterRegionsFilter.Meta.fields

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_columns},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='callingcards',
            url_name='callingcards')
    def callingcards(self, request, *args, **kwargs):
        result_df = callingcards_with_metrics(self.request.query_params)

        # Convert the DataFrame to a list of dictionaries
        data = result_df.to_dict(orient='records')

        # Paginate the data if needed
        paginator = self.paginator
        if paginator is not None:
            paginated_data = paginator.paginate_queryset(data, request)
            return paginator.get_paginated_response(paginated_data)

        # Return the data as a JSON response
        return Response(data)
