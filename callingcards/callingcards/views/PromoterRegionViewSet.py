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
        promoter_res = self.get_queryset()\
            .annotate(promoter_id=F('id'),
                      promoter_source=F('source'))
        promoter_df = pd.DataFrame.from_records(promoter_res.values())
        promoter_df = promoter_df[['promoter_id', 'promoter_source']]

        experiment_res = self.get_queryset()\
            .calling_cards_experiment(**self.request.query_params)
        experiment_df = pd.DataFrame.from_records(experiment_res)
        experiment_df = experiment_df[['promoter_id', 'promoter_source',
                                       'experiment_hops', 'experiment_id']]

        background_res = self.get_queryset()\
            .calling_cards_background(**self.request.query_params)
        background_df = pd.DataFrame.from_records(background_res)
        background_df = background_df[['promoter_id', 'promoter_source',
                                       'background_hops', 'background_source']]
        
        total_hops_dict = {
            'background': {},
            'experiment': {},
        }

        background_df_list = []
        for background in background_df.background_source.unique():
            df = pd.merge(
                promoter_df,
                background_df[background_df.background_source == background],
                on=['promoter_id', 'promoter_source'],
                how='left')

            df.fillna({'background_hops': 0,
                       'background_source': background, },
                      inplace=True)
            
            total_hops_dict['background'][background] = \
                len(df[df.background_hops > 0])
            
            background_df_list.append(df)
        
        promoter_background_df = \
            pd.concat(background_df_list, ignore_index=True)

        experiment_df_list = []
        for experiment in experiment_df.experiment_id.unique():
            df = pd.merge(
                promoter_background_df,
                experiment_df[experiment_df.experiment_id == experiment],
                on=['promoter_id', 'promoter_source'],
                how='left')

            df.fillna({'experiment_hops': 0,
                       'experiment_id': experiment, },
                      inplace=True)
            
            total_hops_dict['experiment'][experiment] = \
                len(df[df.experiment_hops > 0])
            
            experiment_df_list.append(df)

        result_df = pd.concat(experiment_df_list, ignore_index=True)



        # Convert the DataFrame to a list of dictionaries
        data = result_df.to_dict(orient='records')

        # Paginate the data if needed
        paginator = self.paginator
        if paginator is not None:
            paginated_data = paginator.paginate_queryset(data, request)
            return paginator.get_paginated_response(paginated_data)

        # Return the data as a JSON response
        return Response(data)
