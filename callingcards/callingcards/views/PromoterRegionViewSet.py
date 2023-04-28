# pylint: disable=C0209,W1202
import logging
import os
import gzip
import io
import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django_filters import rest_framework as filters
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import pandas as pd

from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import (PromoterRegions, CallingCardsSig,
                      CCExperiment, BackgroundSource,
                      PromoterRegionsSource)
from ..serializers import (PromoterRegionsSerializer,
                           PromoterRegionsTargetsOnlySerializer)
from ..filters import (PromoterRegionsFilter, CCExperimentFilter,
                       CallingCardsSigFilter)
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
        # user the auth token to get the user object
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header:
            # Assuming the header is "Token <token_key>"
            token_key = auth_header.split(" ")[1]
        else:
            return Response("Unauthorized",
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Retrieve the token object and the associated user
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return Response("Invalid token",
                            status=status.HTTP_401_UNAUTHORIZED)

        logger.debug('promoterregions/callingcards queryparams: '
                     '{}'.format(user))

        # first, get all associated experiment_ids
        experiment_id_qs = CCExperimentFilter(
            self.request.query_params,
            queryset=CCExperiment.objects.all())\
            .qs\
            .values_list('id', flat=True)\
            .distinct()
        experiment_id_list = list(experiment_id_qs)
        logger.debug('promoterregions/callingcards experiment_id_list: '
                     '{}'.format(experiment_id_list))

        # iterate over the experiment ids and either get the cached file
        # or calculate the dataframe
        df_list = []
        for experiment in experiment_id_list:
            # check if the file exists in the cache
            cached_sig = CallingCardsSigFilter(
                {'experiment_id': experiment,
                 'background_source': self.request.query_params.get(
                     'background_source', None),
                 'promoter_source': self.request.query_params.get(
                     'promoter_source', None)},
                queryset=CallingCardsSig.objects.all()).qs
            # log the length of the cached file
            logger.debug('promoterregions/callingcards cached_sig len: '
                         '{}'.format(len(cached_sig)))

            # if there are no cached files, calculate the metrics by replicate
            if len(cached_sig) == 0:
                # if not, calculate
                result_df = callingcards_with_metrics(
                    {'experiment_id': experiment,
                        'background_source':
                        self.request.query_params
                            .get('background_source', None),
                        'promoter_source':
                        self.request.query_params
                            .get('promoter_source', None)})
                # cache the result in the database
                grouped = result_df.groupby(['experiment_id',
                                             'background_source',
                                             'promoter_source'])
                for name, group in grouped:
                    logger.debug('promoterregions/callingcards group name: '
                                 '{}'.format(name))
                    experiment_id, background_source, promoter_source = name

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
                        f'ccexperiment_{experiment_id}'
                        f'_{promoter_source}.csv.gz')

                    logger.debug("CallingCardsSig filepath: %s", filepath)

                    default_storage.save(
                        filepath,
                        ContentFile(compressed_buffer.read()))

                    # Close the buffer
                    compressed_buffer.close()

                    # create the record in the database
                    CallingCardsSig.objects.create(
                        uploader=user,
                        uploadDate=datetime.date.today(),
                        modified=datetime.datetime.now(),
                        modifiedBy=user,
                        experiment=CCExperiment.objects.get(pk=experiment_id),
                        background_source=BackgroundSource.objects.get(pk=background_source),  # noqa
                        promoter_source=PromoterRegionsSource.objects.get(pk=promoter_source),  # noqa
                        file=filepath)

                df_list.append(result_df)
            # if there are records already in the database, get them, read
            # them in and append them to the list
            else:
                for significance_file in cached_sig:
                    # Get the file field from the queryset
                    file_field = significance_file.file
                    # Open the file using the storage backend
                    with default_storage.open(file_field.name, 'rb') as f:
                        # Read the file content into a BytesIO buffer
                        file_content = io.BytesIO(f.read())
                    # Read the file content with pandas
                    df = pd.read_csv(file_content, compression='gzip')
                    # append it to the list
                    df_list.append(df)

            # save the dataframe to file (compressed)
            df_concatenated = pd.concat(df_list, ignore_index=True)
            # create a file-like buffer to receive the compressed data
            compressed_buffer = io.BytesIO()

            # compress the dataframe and write it to the buffer
            with gzip.GzipFile(fileobj=compressed_buffer, mode='wb') as gz:
                df_concatenated.to_csv(gz, index=False, encoding='utf-8')

            # create the response object and set its content
            # and content type
            response = HttpResponse(compressed_buffer.getvalue(),
                                    content_type='application/gzip')

            # set the content encoding and filename
            response['Content-Encoding'] = 'gzip'
            response['Content-Disposition'] = \
                'attachment; filename="data.csv.gz"'

            return response
