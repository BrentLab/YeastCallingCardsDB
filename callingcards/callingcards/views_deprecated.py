# pylint: disable=E1101,W0212
"""Calling Cards API Views

To interact with this model via a RESTful API, you can perform the following
    CRUD actions:

    1. Create (POST): To create a new ChrMap object, send a POST request to the
       appropriate API endpoint (e.g., /api/chrmap/) with the required fields
       in the request body as JSON.

    2. Read (GET): To retrieve an existing ChrMap object, send a GET request
      to the specific API endpoint (e.g., /api/chrmap/<id>/) using the
      object's ID. To list all ChrMap objects, send a GET request to the
      list endpoint (e.g., /api/chrmap/).

    3. Update (PUT/PATCH): To update an existing ChrMap object, send a PUT (for
       a complete update) or PATCH (for a partial update) request to the
       specific API endpoint (e.g., /api/chrmap/<id>/) with the updated
       fields in the request body as JSON.

    4. Delete (DELETE): To delete an existing ChrMap object, send a DELETE
       request to the specific API endpoint (e.g., /api/chrmap/<id>/).
"""
import logging
import io
import csv

from django_filters import rest_framework as filters
from django.conf import settings
from django.db import DatabaseError
from django.db.models.functions import Coalesce, NullIf
from django.db.models import (Max, F, Q, Subquery, OuterRef,
                              Count, Value, Case, When, CharField,
                              ForeignKey, QuerySet)
from rest_framework.settings import api_settings
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from celery.result import AsyncResult

from callingcards.celery import app


# from .filters import (McIsaacZevFilter, KemmerenTfkoFilter,
#                       CCExperimentFilter, HopsReplicateSigFilter, GeneFilter,
#                       PromoterRegionsFilter, HarbisonChIPFilter,
#                       QcMetricsFilter, QcManualReviewFilter,
#                       QcR1ToR2TfFilter, QcR2ToR1TfFilter,
#                       QcTfToTransposonFilter)

# from .models import (ChrMap, Gene, PromoterRegions, HarbisonChIP,
#                      KemmerenTFKO, McIsaacZEV, Background, CCTF,
#                      CCExperiment, Hops, HopsReplicateSig, QcMetrics,
#                      QcManualReview, QcR1ToR2Tf, QcR2ToR1Tf,
#                      QcTfToTransposon)

# from .serializers import (ChrMapSerializer, GeneSerializer,
#                           PromoterRegionsSerializer,
#                           PromoterRegionsTargetsOnlySerializer,
#                           HarbisonChIPSerializer,
#                           HarbisonChIPAnnotatedSerializer,
#                           KemmerenTFKOSerializer, McIsaacZEVSerializer,
#                           BackgroundSerializer, CCTFSerializer,
#                           CCTFListSerializer,
#                           CCExperimentSerializer, HopsSerializer,
#                           HopsReplicateSigSerializer,
#                           HopsReplicateSigAnnotatedSerializer,
#                           QcMetricsSerializer, QcManualReviewSerializer,
#                           QcR1ToR2TfSerializer, QcR2ToR1TfSerializer,
#                           QcTfToTransposonSerializer,
#                           BarcodeComponentsSummarySerializer,
#                           QcReviewSerializer, ExpressionViewSetSerializer)

# from .tasks import process_upload, upload_csv_postgres_task

# # this can be used if you need to log a queryset
# from .utils import compute_cc_effect

# logger = logging.getLogger(__name__)

# __all__ = ['ChrMapViewSet', 'GeneViewSet', 'PromoterRegionsViewSet',
#            'HarbisonChIPViewSet', 'KemmerenTFKOViewSet', 'McIsaacZEVViewSet',
#            'BackgroundViewSet', 'CCTFViewSet', 'CCExperimentViewSet',
#            'HopsViewSet', 'HopsReplicateSigViewSet', 'QcMetricsViewSet',
#            'QcManualReviewViewSet', 'QcR1ToR2ViewSet',
#            'QcR2ToR1ViewSet', 'QcTfToTransposonViewSet',
#            'QcR1ToR2TfSummaryViewSet', 'QcReviewViewSet',
#            'ExpressionViewSet']

# # NOTE this is used in QcReviewViewSet and in the data itself to identify
# # an unknown barcode in a given run
# UNDETERMINED_LOCUS_TAG = 'undetermined'




# # class ChrMapViewSet(ListModelFieldsMixin,
# #                     CustomCreateMixin,
# #                     PageSizeModelMixin,
# #                     viewsets.ModelViewSet,
# #                     CountModelMixin):
# #     """
# #     ChrMapViewSet is a Django viewset for the ChrMap model. It provides 
# #       a RESTful API for clients to interact with ChrMap objects, including 
# #       creating, reading, updating, and deleting instances.

# #     Inheritance:
# #         ListModelFieldsMixin: Provides a mixin to list all available fields 
# #           for the model.
# #         CustomCreateMixin: Allows for custom creation of instances.
# #         PageSizeModelMixin: Provides a mixin to handle pagination and 
# #           page size.
# #         viewsets.ModelViewSet: A base class for generic model viewsets.
# #         CountModelMixin: Provides a mixin to return the total count 
# #           of objects.

# #     Attributes:
# #         queryset: The base queryset for this viewset. Retrieves all ChrMap 
# #           objects and orders them by their ID.
# #         serializer_class: The serializer to use for handling ChrMap objects. 
# #         permission_classes: Defines the permission classes for this viewset.
# #                             Allows any user to access this viewset.

# #     API Endpoints:
# #         1. List: GET /api/chrmap/ - Retrieves a paginated list of all 
# #            ChrMap objects.
# #         2. Create: POST /api/chrmap/ - Creates a new ChrMap object with 
# #           the provided data.
# #         3. Retrieve: GET /api/chrmap/<id>/ - Retrieves a specific ChrMap 
# #           object by ID.
# #         4. Update: PUT/PATCH /api/chrmap/<id>/ - Updates a specific ChrMap 
# #           object by ID.
# #         5. Delete: DELETE /api/chrmap/<id>/ - Deletes a specific ChrMap 
# #           object by ID.
# #     """
# #     queryset = ChrMap.objects.all().order_by('id')  # noqa
# #     serializer_class = ChrMapSerializer  # noqa
# #     permission_classes = (AllowAny,)


# # class GeneViewSet(ListModelFieldsMixin,
# #                   CustomCreateMixin,
# #                   PageSizeModelMixin,
# #                   viewsets.ModelViewSet,
# #                   CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = Gene.objects.all().order_by('id')
# #     serializer_class = GeneSerializer
# #     permission_classes = (AllowAny,)

# #     filterset_class = GeneFilter
# #     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
# #     search_fields = ['locus_tag', 'gene']


# # class PromoterRegionsViewSet(ListModelFieldsMixin,
# #                              CustomCreateMixin,
# #                              PageSizeModelMixin,
# #                              viewsets.ModelViewSet,
# #                              CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = PromoterRegions.objects.all().order_by('id')  # noqa
# #     serializer_class = PromoterRegionsSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = PromoterRegionsFilter

# #     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
# #     search_fields = ['associated_feature__locus_tag',
# #                      'associated_feature__gene', 'source']

# #     @action(detail=False, methods=['get'], url_path='targets',
# #             url_name='targets')
# #     def targets(self, request, *args, **kwargs):
# #         targets_queryset = PromoterRegions.objects\
# #             .targets()\
# #             .order_by('id')

# #         # Apply the filtering
# #         filtered_queryset = self.filter_queryset(targets_queryset)

# #         page = self.paginate_queryset(filtered_queryset)
# #         if page is not None:
# #             serializer = PromoterRegionsTargetsOnlySerializer(page, many=True)
# #             return self.get_paginated_response(serializer.data)

# #         serializer = PromoterRegionsTargetsOnlySerializer(filtered_queryset,
# #                                                           many=True)
# #         return Response(serializer.data)

# #     @action(detail=False, url_path='targets/count',
# #             url_name='targets-count')
# #     def targets_count(self, request, *args, **kwargs) -> Response:
# #         annote_qs = PromoterRegions.objects.targets()
# #         annote_qs_fltr = PromoterRegionsFilter(
# #             self.request.GET,
# #             queryset=annote_qs)
# #         content = {'count': self.get_count(annote_qs_fltr.qs)}
# #         return Response(content)

# #     @action(detail=False, url_path='targets/pagination_info',
# #             url_name='targets-pagination-info')
# #     def targets_pagination_info(self, request,
# #                                 *args, **kwargs) -> Response:
# #         return self.pagination_info(request, *args, **kwargs)

# #     @action(detail=False, methods=['get'], url_path='targets/fields',
# #             url_name='targets-fields')
# #     def targets_fields(self, request, *args, **kwargs):
# #         readable = [field.source for field in
# #                     PromoterRegionsTargetsOnlySerializer()._readable_fields]
# #         writable = None
# #         automatically_generated = None
# #         filter_columns = PromoterRegionsFilter.Meta.fields

# #         # Return the readable fields as a JSON response
# #         return Response({"readable": readable,
# #                          "writable": writable,
# #                          "automatically_generated":
# #                          automatically_generated,
# #                          "filter": filter_columns},
# #                         status=status.HTTP_200_OK)


# # class HarbisonChIPViewSet(ListModelFieldsMixin,
# #                           CustomCreateMixin,
# #                           PageSizeModelMixin,
# #                           viewsets.ModelViewSet,
# #                           CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = HarbisonChIP.objects.all().order_by('id')  # noqa
# #     serializer_class = HarbisonChIPSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = HarbisonChIPFilter

# #     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
# #     search_fields = ['associated_feature__locus_tag',
# #                      'associated_feature__gene', 'source']

# #     @action(detail=False, methods=['get'], url_path='with_annote',
# #             url_name='with-annote')
# #     def with_annotations(self, request, *args, **kwargs):
# #         annotated_queryset = HarbisonChIP.objects\
# #             .with_annotations().order_by('id')

# #         # Apply the filtering
# #         filtered_queryset = self.filter_queryset(annotated_queryset)

# #         page = self.paginate_queryset(filtered_queryset)
# #         if page is not None:
# #             serializer = HarbisonChIPAnnotatedSerializer(page, many=True)
# #             return self.get_paginated_response(serializer.data)

# #         serializer = HarbisonChIPAnnotatedSerializer(
# #             filtered_queryset, many=True)
# #         return Response(serializer.data)

# #     @action(detail=False, url_path='with_annote/count',
# #             url_name='with-annote-count')
# #     def with_annotations_count(self, request, *args, **kwargs) -> Response:
# #         annote_qs = HarbisonChIP.objects.with_annotations()
# #         annote_qs_fltr = HarbisonChIPFilter(
# #             self.request.GET,
# #             queryset=annote_qs)
# #         content = {'count': self.get_count(annote_qs_fltr.qs)}
# #         return Response(content)

# #     @action(detail=False, url_path='with_annote/pagination_info',
# #             url_name='with-annote-pagination-info')
# #     def with_annotations_pagination_info(self, request,
# #                                          *args, **kwargs) -> Response:
# #         return self.pagination_info(request, *args, **kwargs)

# #     @action(detail=False, methods=['get'], url_path='with_annote/fields',
# #             url_name='with-annote-fields')
# #     def with_annotation_fields(self, request, *args, **kwargs):
# #         # Get the _readable_fields attribute of the
# #         # HarbisonChIPAnnotatedSerializer instance
# #         readable = [field.source for field in
# #                     HarbisonChIPAnnotatedSerializer()._readable_fields]
# #         writable = None
# #         automatically_generated = None
# #         filter_columns = HarbisonChIPFilter.Meta.fields

# #         # Return the readable fields as a JSON response
# #         return Response({"readable": readable,
# #                          "writable": writable,
# #                          "automatically_generated":
# #                          automatically_generated,
# #                          "filter": filter_columns},
# #                         status=status.HTTP_200_OK)


# # class KemmerenTFKOViewSet(ListModelFieldsMixin,
# #                           CustomCreateMixin,
# #                           PageSizeModelMixin,
# #                           viewsets.ModelViewSet,
# #                           CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = KemmerenTFKO.objects.all().order_by('id')  # noqa
# #     serializer_class = KemmerenTFKOSerializer  # noqa
# #     permission_classes = (AllowAny,)

# #     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
# #     search_fields = ['tf__locus_tag', 'tf__gene',
# #                      'gene__locus_tag', 'gene__gene']

# #     filterset_class = KemmerenTfkoFilter


# # class McIsaacZEVViewSet(ListModelFieldsMixin,
# #                         CustomCreateMixin,
# #                         PageSizeModelMixin,
# #                         viewsets.ModelViewSet,
# #                         CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = McIsaacZEV.objects.all().order_by('id')  # noqa
# #     serializer_class = McIsaacZEVSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = McIsaacZevFilter

# #     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
# #     search_fields = ['tf__locus_tag', 'tf__gene',
# #                      'gene__locus_tag', 'gene__gene']


# # class BackgroundViewSet(ListModelFieldsMixin,
# #                         CustomCreateMixin,
# #                         PageSizeModelMixin,
# #                         viewsets.ModelViewSet,
# #                         CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = Background.objects.all().order_by('id')  # noqa
# #     serializer_class = BackgroundSerializer  # noqa
# #     permission_classes = (AllowAny,)


# # class CCTFViewSet(ListModelFieldsMixin,
# #                   CustomCreateMixin,
# #                   PageSizeModelMixin,
# #                   viewsets.ModelViewSet,
# #                   CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = CCTF.objects.all().order_by('id')  # noqa
# #     serializer_class = CCTFSerializer  # noqa
# #     permission_classes = (AllowAny,)

# #     @action(detail=False, methods=['get'], url_path='tf_list',
# #             url_name='tf-list')
# #     def tf_list(self, request, *args, **kwargs):
# #         queryset = self.get_queryset()

# #         page = self.paginate_queryset(queryset)
# #         if page is not None:
# #             serializer = self.get_serializer(page, many=True)
# #             return self.get_paginated_response(serializer.data)

# #         serializer = self.get_serializer(queryset, many=True)
# #         return Response(serializer.data)

# #     @action(detail=False, url_path='tf_list/count',
# #             url_name='tf-list-count')
# #     def effects_count(self, request, *args, **kwargs) -> Response:
# #         return self.count(request, *args, **kwargs)

# #     @action(detail=False, url_path='tf_list/pagination_info',
# #             url_name='tf-list-pagination-info')
# #     def effects_pagination_info(self, request,
# #                                 *args, **kwargs) -> Response:
# #         return self.pagination_info(request, *args, **kwargs)

# #     @action(detail=False, methods=['get'], url_path='tf_list/fields',
# #             url_name='tf-list-fields')
# #     def effects_fields(self, request, *args, **kwargs):
# #         filter_fields = None
# #         return self.fields(request, *args, filter_fields=filter_fields)

# #     def get_queryset(self):
# #         if 'tf_list' in self.request.path_info:
# #             return CCTF.objects.tf_list()
# #         else:
# #             return CCTF.objects.all().order_by('id')

# #     def get_serializer_class(self):
# #         if 'tf_list' in self.request.path_info:
# #             return CCTFListSerializer
# #         else:
# #             return CCTFSerializer


# # class CCExperimentViewSet(ListModelFieldsMixin,
# #                           CustomCreateMixin,
# #                           PageSizeModelMixin,
# #                           viewsets.ModelViewSet,
# #                           CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = CCExperiment.objects.all().order_by('id')  # noqa
# #     serializer_class = CCExperimentSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = CCExperimentFilter


# # class HopsViewSet(ListModelFieldsMixin,
# #                   CustomCreateMixin,
# #                   PageSizeModelMixin,
# #                   viewsets.ModelViewSet,
# #                   CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = Hops.objects.all().order_by('id')  # noqa
# #     serializer_class = HopsSerializer  # noqa
# #     permission_classes = (AllowAny,)


# # class HopsReplicateSigViewSet(ListModelFieldsMixin,
# #                               CustomCreateMixin,
# #                               PageSizeModelMixin,
# #                               viewsets.ModelViewSet,
# #                               CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = HopsReplicateSig.objects.all().order_by('id')  # noqa
# #     serializer_class = HopsReplicateSigSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = HopsReplicateSigFilter

# #     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
# #     search_fields = ['promoterregions__associated_features__locus_tag',
# #                      'promoterregions___associated_features__gene',
# #                      'experiment__tf__tf__locus_tag',
# #                      'experiment___tf__tf__gene']

# #     @action(detail=False, methods=['get'], url_path='with_annote',
# #             url_name='with-annote')
# #     def with_annotations(self, request, *args, **kwargs):
# #         annotated_queryset = HopsReplicateSig.objects\
# #             .with_annotations().order_by('id')

# #         # Apply the filtering
# #         filtered_queryset = self.filter_queryset(annotated_queryset)

# #         page = self.paginate_queryset(filtered_queryset)
# #         if page is not None:
# #             serializer = HopsReplicateSigAnnotatedSerializer(page, many=True)
# #             return self.get_paginated_response(serializer.data)

# #         serializer = HopsReplicateSigAnnotatedSerializer(filtered_queryset,
# #                                                          many=True)
# #         return Response(serializer.data)

# #     @action(detail=False, url_path='with_annote/count',
# #             url_name='with-annote-count')
# #     def with_annotations_count(self, request, *args, **kwargs) -> Response:
# #         hops_with_annotations = HopsReplicateSig\
# #             .objects.with_annotations()
# #         hops_with_annotations_fltr = HopsReplicateSigFilter(
# #             self.request.GET,
# #             queryset=hops_with_annotations)
# #         content = {'count': self.get_count(hops_with_annotations_fltr.qs)}
# #         return Response(content)

# #     @action(detail=False, url_path='with_annote/pagination_info',
# #             url_name='with-annote-pagination-info')
# #     def with_annotations_pagination_info(self, request,
# #                                          *args, **kwargs) -> Response:
# #         return self.pagination_info(request, *args, **kwargs)

# #     @action(detail=False, url_path='with_annote/fields',
# #             url_name='with-annote-fields')
# #     def with_annotations_fields(self, request, *args, **kwargs) -> Response:
# #         # Use GeneWithEffectsSerializer instead of DummySerializer
# #         readable = [field.source for field in
# #                     HopsReplicateSigAnnotatedSerializer()._readable_fields]
# #         writable = None
# #         automatically_generated = ['id',
# #                                    'uploader',
# #                                    'uploadDate',
# #                                    'modified']

# #         filter_columns = HopsReplicateSigFilter.Meta.fields

# #         # Return the readable fields as a JSON response
# #         return Response({"readable": readable,
# #                         "writable": writable,
# #                          "automatically_generated":
# #                          automatically_generated,
# #                          "filter": filter_columns},
# #                         status=status.HTTP_200_OK)


# # class QcMetricsViewSet(ListModelFieldsMixin,
# #                        CustomCreateMixin,
# #                        PageSizeModelMixin,
# #                        viewsets.ModelViewSet,
# #                        CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = QcMetrics.objects.all().order_by('id')  # noqa
# #     serializer_class = QcMetricsSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = QcMetricsFilter


# # class QcManualReviewViewSet(ListModelFieldsMixin,
# #                             CustomCreateMixin,
# #                             PageSizeModelMixin,
# #                             viewsets.ModelViewSet,
# #                             CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = QcManualReview.objects.all().order_by('id')  # noqa
# #     serializer_class = QcManualReviewSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = QcManualReviewFilter


# # class QcR1ToR2ViewSet(ListModelFieldsMixin,
# #                       CustomCreateMixin,
# #                       PageSizeModelMixin,
# #                       viewsets.ModelViewSet,
# #                       CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = QcR1ToR2Tf.objects.all().order_by('id')  # noqa
# #     serializer_class = QcR1ToR2TfSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = QcR1ToR2TfFilter


# # class QcR2ToR1ViewSet(ListModelFieldsMixin,
# #                       CustomCreateMixin,
# #                       PageSizeModelMixin,
# #                       viewsets.ModelViewSet,
# #                       CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = QcR2ToR1Tf.objects.all().order_by('id')  # noqa
# #     serializer_class = QcR2ToR1TfSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = QcR2ToR1TfFilter


# # class QcTfToTransposonViewSet(ListModelFieldsMixin,
# #                               CustomCreateMixin,
# #                               PageSizeModelMixin,
# #                               viewsets.ModelViewSet,
# #                               CountModelMixin):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = QcTfToTransposon.objects.all().order_by('id')  # noqa
# #     serializer_class = QcTfToTransposonSerializer  # noqa
# #     permission_classes = (AllowAny,)
# #     filterset_class = QcTfToTransposonFilter


# # class QcR1ToR2TfSummaryViewSet(viewsets.ViewSet):
# #     def list(self, request):

# #         r1_r2_max_tally_subquery = QcR1ToR2Tf.objects.filter(
# #             experiment_id=OuterRef('pk')
# #         ).order_by('-tally').values('edit_dist')[:1]

# #         r2_r1_max_tally_subquery = QcR2ToR1Tf.objects.filter(
# #             experiment_id=OuterRef('pk')
# #         ).order_by('-tally').values('edit_dist')[:1]

# #         query = (
# #             CCExperiment.objects
# #             .annotate(
# #                 experiment_id=F('id'),
# #                 r1_r2_max_tally=Max('qcr1tor2tf__tally'),
# #                 r1_r2_status=Subquery(r1_r2_max_tally_subquery),
# #                 r2_r1_max_tally=Max('qcr2tor1tf__tally'),
# #                 r2_r1_status=Subquery(r2_r1_max_tally_subquery),
# #             )
# #             .filter(Q(r1_r2_max_tally__isnull=False)
# #                     | Q(r2_r1_max_tally__isnull=False))
# #             .order_by('experiment_id')
# #             .values('experiment_id', 'r1_r2_status', 'r2_r1_status')
# #         )

# #         for item in query:
# #             item['r1_r2_status'] = 'pass' if \
# #                 item['r1_r2_status'] == 0 else 'fail'
# #             item['r2_r1_status'] = 'pass' if \
# #                 item['r2_r1_status'] == 0 else 'fail'

# #         serializer = BarcodeComponentsSummarySerializer(query, many=True)
# #         return Response(serializer.data)


# # class QcReviewViewSet(ListModelFieldsMixin,
# #                       CustomCreateMixin,
# #                       PageSizeModelMixin,
# #                       viewsets.ModelViewSet,
# #                       CountModelMixin):

# #     serializer_class = QcReviewSerializer

# #     filter_backends = [filters.DjangoFilterBackend]

# #     filterset_class = CCExperimentFilter

# #     def get_queryset(self):

# #         hop_count_subquery = Hops.objects\
# #             .filter(experiment_id=OuterRef('pk'))\
# #             .values('experiment_id')\
# #             .annotate(count=Count('experiment_id'))\
# #             .values('count')

# #         r1_r2_max_tally_edit_dist_subquery = QcR1ToR2Tf.objects.filter(
# #             experiment_id=OuterRef('pk')
# #         ).order_by('-tally').values('edit_dist')[:1]

# #         r2_r1_max_tally_edit_dist_subquery = QcR2ToR1Tf.objects.filter(
# #             experiment_id=OuterRef('pk')
# #         ).order_by('-tally').values('edit_dist')[:1]

# #         unknown_feature_id = Gene.objects\
# #             .get(locus_tag=UNDETERMINED_LOCUS_TAG).id

# #         ccexperiment_fltr = CCExperimentFilter(self.request.GET)

# #         # TODO add select/prefetch related to reduce the number of queries
# #         # note when teh qc_metrics unmapped is 0, set to 0 to avoid divide by
# #         # 0 error
# #         query = (
# #             ccexperiment_fltr.qs
# #             .exclude(tf_id=unknown_feature_id)
# #             .annotate(
# #                 experiment_id=F('id'),
# #                 tf_alias=Case(
# #                     When(tf__tf__gene__istartswith='unknown',
# #                             then=F('tf__tf__locus_tag')),
# #                     default=F('tf__tf__gene'),
# #                     output_field=CharField()),
# #                 r1_r2_max_tally_edit_dist=Subquery(r1_r2_max_tally_edit_dist_subquery),  # noqa
# #                 r2_r1_max_tally_edit_dist=Subquery(r2_r1_max_tally_edit_dist_subquery),  # noqa
# #                 map_unmap_ratio=Coalesce(
# #                     F('qcmetrics__genome_mapped') / NullIf(
# #                         F('qcmetrics__unmapped'), 0), Value(0)
# #                 ),
# #                 num_hops=Subquery(hop_count_subquery),
# #                 rank_recall=F('qcmanualreview__rank_recall'),
# #                 chip_better=F('qcmanualreview__chip_better'),
# #                 data_usable=F('qcmanualreview__data_usable'),
# #                 passing_replicate=F('qcmanualreview__passing_replicate'),
# #                 note=F('qcmanualreview__note')
# #             )
# #             .order_by('tf_alias', 'batch', 'batch_replicate')
# #             .values('experiment_id', 'tf_alias', 'batch', 'batch_replicate',
# #                     'r1_r2_max_tally_edit_dist', 'r2_r1_max_tally_edit_dist',
# #                     'map_unmap_ratio', 'num_hops', 'rank_recall',
# #                     'chip_better', 'data_usable', 'passing_replicate', 'note')
# #         )

# #         # for item in query:
# #         #     item['r1_r2_status'] = 'pass' if item['r1_r2_status'] == 0 \
# #         #         else 'fail'
# #         #     item['r2_r1_status'] = 'pass' if item['r2_r1_status'] == 0 \
# #         #         else 'fail'

# #         return query

# #     def update(self, request, pk=None):

# #         manual_review = QcManualReview.objects.get(pk=pk)

# #         qc_review_combined = self.get_queryset().get(experiment_id=pk)
# #         qc_review_combined_data = QcReviewSerializer(qc_review_combined).data

# #         # Get the fields that are present in the QcManualReviewSerializer
# #         valid_fields = set(QcManualReviewSerializer().get_fields().keys())

# #         # Get the data fields to update and filter out any invalid fields
# #         # TODO this expects a single dict, not a list. Should it accept a list?
# #         # unlisting and extracting the first item is what the [0] is doing
# #         update_data = {key: value for key, value in
# #                        request.data[0].items() if key in valid_fields}

# #         serializer = QcManualReviewSerializer(
# #             manual_review,
# #             data=update_data,
# #             partial=True)

# #         if serializer.is_valid():
# #             serializer.save()
# #             qc_review_combined_data.update(serializer.data)
# #             drop_keys_list = ['experiment', 'id']
# #             for key in drop_keys_list:
# #                 qc_review_combined_data.pop(key, None)
# #             response = Response(qc_review_combined_data, status=201)
# #             response['Cache-Control'] = 'no-cache'
# #         else:
# #             response = Response({
# #                 'error': 'Invalid data',
# #                 'data': update_data,
# #                 'errors': serializer.errors
# #             }, status=400)

# #         return response


# # class ExpressionViewSet(ListModelFieldsMixin,
# #                                CustomCreateMixin,
# #                                PageSizeModelMixin,
# #                                viewsets.ModelViewSet,
# #                                CountModelMixin):
# #     """
# #     ExpressionViewSet returns gene expression data for genes
# #     that have both McIsaac ZEV and Kemmeren TF-KO effect values.
# #     """
# #     serializer_class = ExpressionViewSetSerializer

# #     filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
# #     ordering_fields = ['source_expr', 'tf_expr', 'rank_expr']
# #     custom_filter_columns = ['tf_id', 'gene_id', 'effect',
# #                              'tf_locus_tag', 'tf_gene', 'target_locus_tag',
# #                              'target_gene']

# #     def get_queryset(self):

# #         return_fields = ['tf_id_alias', 'tf_locus_tag', 'tf_gene',
# #                          'target_gene_id', 'target_locus_tag', 'target_gene',
# #                          'effect_expr', 'p_expr', 'source_expr']

# #         # Get query parameters for filtering
# #         mcisaac_filter = McIsaacZevFilter(self.request.GET)
# #         kemmeren_filter = KemmerenTfkoFilter(self.request.GET)

# #         mcisaac_filtered_qs = mcisaac_filter.qs\
# #             .annotate(
# #                 tf_id_alias=F('tf_id'),
# #                 tf_locus_tag=F('tf_id__locus_tag'),
# #                 tf_gene=F('tf_id__gene'),
# #                 target_gene_id=F('gene_id'),
# #                 target_locus_tag=F('gene_id__locus_tag'),
# #                 target_gene=F('gene_id__gene'),
# #                 effect_expr=F('effect'),
# #                 p_expr=F('pval'),
# #                 source_expr=Value('mcisaac_zev'))\
# #             .values(*return_fields)

# #         kemmeren_filtered_qs = kemmeren_filter.qs\
# #             .annotate(
# #                 tf_id_alias=F('tf_id'),
# #                 tf_locus_tag=F('tf_id__locus_tag'),
# #                 tf_gene=F('tf_id__gene'),
# #                 target_gene_id=F('gene_id'),
# #                 target_locus_tag=F('gene_id__locus_tag'),
# #                 target_gene=F('gene_id__gene'),
# #                 effect_expr=F('effect'),
# #                 p_expr=F('padj'),
# #                 source_expr=Value('kemmeren_tfko'))\
# #             .values(*return_fields)

# #         # Combine the two querysets and order by 'tf' and 'gene'
# #         concatenated_query = mcisaac_filtered_qs\
# #             .union(kemmeren_filtered_qs)\
# #             .order_by('source_expr', 'tf_id_alias')

# #         return concatenated_query

# #     @action(detail=False, methods=['get'])
# #     def fields(self, request, *args, **kwargs):

# #         # Get the _readable_fields attribute of the dummy serializer instance
# #         readable = ['tf_alias', 'gene_alias', 'effect_expr',
# #                     'p_expr', 'source_expr']
# #         writable = None
# #         automatically_generated = None

# #         try:
# #             filter_columns = self.filterset_class.Meta.fields
# #         except AttributeError:
# #             # Use the custom_filter_columns attribute if available
# #             # this needs to be set in the viewset class when there is no
# #             # filterset_class
# #             filter_columns = getattr(self, 'custom_filter_columns', None)

# #         # Return the readable fields as a JSON response
# #         return Response({"readable": readable,
# #                          "writable": writable,
# #                          "automatically_generated":
# #                          automatically_generated,
# #                          "filter": filter_columns},
# #                         status=status.HTTP_200_OK)

# # class PromoterHopsBackgroundViewQuerySet(QuerySet):
# #     def with_counts(self, experiment_id, background_source,
# #                     consider_strand=False, pseudocount=0.2):
# #         # Calculate total_expression_hops and total_background_hops
# #         total_expression_hops = Hops.objects\
# #             .filter(experiment_id=experiment_id).count()
# #         total_background_hops = Background.objects\
# #             .filter(source=background_source).count()

# #         # Filter and annotate depending on whether the strand should
# #         # be considered
# #         if consider_strand:
# #             strand_condition = Q(strand=F('associated_feature__strand'))
# #         else:
# #             strand_condition = Q()

# #         expression_hops = Hops.objects.filter(
# #             chr=F('associated_feature__chr'),
# #             start__gte=F('associated_feature__start'),
# #             end__lte=F('associated_feature__end'),
# #             experiment_id=experiment_id,
# #             **strand_condition
# #         ).annotate(
# #             promoter_id=F('associated_feature__genepromoter'),
# #         ).values('promoter_id').annotate(
# #             expression_hops=Count('*'),
# #         )

# #         background_hops = Background.objects.filter(
# #             chr=F('associated_feature__chr'),
# #             start__gte=F('associated_feature__start'),
# #             end__lte=F('associated_feature__end'),
# #             source=background_source,
# #             **strand_condition
# #         ).annotate(
# #             promoter_id=F('associated_feature__genepromoter'),
# #         ).values('promoter_id').annotate(
# #             background_hops=Count('*'),
# #         )

# #         return self.annotate(
# #             expression_hops=Subquery(expression_hops.values('expression_hops')[:1]),
# #             background_hops=Subquery(background_hops.values('background_hops')[:1]),
# #         ).annotate(
# #             effect=compute_cc_effect(
# #                 F('expression_hops'),
# #                 total_expression_hops,
# #                 F('background_hops'),
# #                 total_background_hops,
# #                 pseudocount
# #             ),
# #         )


# # class PromoterHopsBackgroundAPIView(APIView):
# #     def get(self, request, *args, **kwargs):
# #         experiment_id = request.GET.get('experiment_id')
# #         background_source = request.GET.get('background_source')
# #         consider_strand = request.GET.get('consider_strand', 'true').lower() == 'true'
# #         pseudocount = float(request.GET.get('pseudocount', 0.2))

# #         queryset = PromoterRegions.objects.with_counts(
# #             experiment_id=experiment_id,
# #             background_source=background_source,
# #             consider_strand=consider_strand,
# #             pseudocount=pseudocount
# #         )

# #         serializer = PromoterHopsBackgroundViewSerializer(queryset, many=True)
# #         return Response(serializer.data)


# # TASK_STATE_DESCRIPTIONS = {
# #     'PENDING': 'The task is waiting for execution or unknown.',
# #     'STARTED': 'The task has been started.',
# #     'SUCCESS': 'The task completed successfully.',
# #     'FAILURE': 'The task resulted in an error.',
# #     'REVOKED': 'The task has been canceled by the user.',
# #     'RETRY': 'The task is being retried after a failure.',
# # }

# # class TaskStatusViewSet(ListModelMixin, viewsets.GenericViewSet):
# #     def get_queryset(self):
# #         return []

# #     def list(self, request, *args, **kwargs):
# #         i = app.control.inspect()

# #         tasks = []
# #         active_tasks = i.active()
# #         if active_tasks:
# #             active_tasks = active_tasks.values()
# #             for worker_tasks in active_tasks:
# #                 for task in worker_tasks:
# #                     task_result = AsyncResult(task['id'])
# #                     status = task_result.status
# #                     tasks.append({
# #                         'task_id': task['id'],
# #                         'endpoint': task['name'],
# #                         'status': status,
# #                         'description': TASK_STATE_DESCRIPTIONS.get(status, "Unknown")
# #                     })

# #         return Response(tasks)
