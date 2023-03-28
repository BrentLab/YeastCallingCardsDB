"""Calling Cards API Views

To interact with this model via a RESTful API, you can perform the following
    CRUD actions:

    1. Create (POST): To create a new ChrMap object, send a POST request to the
       appropriate API endpoint (e.g., /api/chrmaps/) with the required fields
       in the request body as JSON.

    2. Read (GET): To retrieve an existing ChrMap object, send a GET request to
       the specific API endpoint (e.g., /api/chrmaps/<id>/) using the object's ID.
       To list all ChrMap objects, send a GET request to the list endpoint (e.g.,
       /api/chrmaps/).

    3. Update (PUT/PATCH): To update an existing ChrMap object, send a PUT (for
       a complete update) or PATCH (for a partial update) request to the specific
       API endpoint (e.g., /api/chrmaps/<id>/) with the updated fields in the
       request body as JSON.

    4. Delete (DELETE): To delete an existing ChrMap object, send a DELETE
       request to the specific API endpoint (e.g., /api/chrmaps/<id>/).
"""
import logging

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from django.conf import settings
from rest_framework.settings import api_settings
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Max, F, Q, Subquery, OuterRef,\
    Count, Value, Case, When, CharField

from .filters import McIsaacZevFilter, KemmerenTfkoFilter, \
    CCExperimentFilter, HopsReplicateSigFilter, GeneFilter, \
    PromoterRegionsFilter, HarbisonChIPFilter

from .models import *

from .serializers import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['ChrMapViewSet', 'GeneViewSet', 'PromoterRegionsViewSet',
           'HarbisonChIPViewSet', 'KemmerenTFKOViewSet', 'McIsaacZEVViewSet',
           'BackgroundViewSet', 'CCTFViewSet', 'CCExperimentViewSet',
           'HopsViewSet', 'HopsReplicacteSigViewSet', 'QcMetricsViewSet',
           'QcManualReviewViewSet', 'QcR1ToR2ViewSet',
           'QcR2ToR1ViewSet', 'QcTfToTransposonViewSet',
           'QcR1ToR2TfSummaryViewSet', 'QcReviewViewSet',
           'ExpressionViewSetViewSet']

# NOTE this is used in QcReviewViewSet and in the data itself to identify
# an unknown barcode in a given run
UNDETERMINED_LOCUS_TAG = 'undetermined'


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

    @property
    def user_field(self):
        """user field is the field from the model that will be
          set to the current user. defaults to "uploder" """
        return self._user_field or 'uploader'

    @user_field.setter
    def user_field(self, value):
        self._user_field = value

    def create(self, request, *args, **kwargs):
        """ overwrite default create to accept either single or mulitple
        records on create/update
            cite: https://stackoverflow.com/a/65078963/9708266
            accept either an array or a single object,
            eg {"field1": "", "field2": "", ...} or
            [{"field1": "", "field2": "", ...},
            {"field1": "", "field2": "", ...}, ...]
        """
        many_flag = True if isinstance(request.data, list) else False

        kwargs = {
            self.user_field: self.request.user
        }

        serializer = self.get_serializer(data=request.data, many=many_flag)
        serializer.is_valid(raise_exception=True)
        serializer.save(**kwargs)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


class CountModelMixin(object):
    """
    Count a mocel viewset queryset.
    Cite: https://stackoverflow.com/a/49709157/9708266
    """

    def get_count(self, queryset):
        return queryset.count()

    @action(detail=False, methods=['get'])
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)

class ViewRowCountMixin(object):
    """this will add a count action to viewsets which are not model viewsets"""
    @action(detail=False, methods=['get'])
    def count(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        count = len(response.data)
        return Response({"count": count})


class PageSizeModelMixin(object):
    """
    Add a page size limit action to viewsets.
    """
    @action(detail=False, methods=['get'])
    def pagination_info(self, request, *args, **kwargs):
        """
        Return the maximum page size limit for paginated requests.
        """
        default_page_size = api_settings.PAGE_SIZE
        page_size_limit = settings.REST_FRAMEWORK.get('PAGE_SIZE', None)

        return Response({
            'default_page_size': default_page_size,
            'page_size_limit': page_size_limit})


class ListModelFieldsMixin:
    @action(detail=False, methods=['get'])
    def fields(self, request, *args, **kwargs):
        # Define a dummy serializer class for the model
        # associated with the viewset
        class DummySerializer(ModelSerializer):
            class Meta:
                model = self.queryset.model
                fields = '__all__'

        # Get the _readable_fields attribute of the dummy serializer instance
        readable = [field.source for field in
                    DummySerializer()._readable_fields]
        writable = [field.source for field in
                    DummySerializer()._writable_fields]
        automatically_generated = ['id',
                                   'uploader',
                                   'uploadDate',
                                   'modified']

        try:
            filter_columns = self.filterset_class.Meta.fields
        except AttributeError:
            # Use the custom_filter_columns attribute if available
            # this needs to be set in the viewset class when there is no
            # filterset_class
            filter_columns = getattr(self, 'custom_filter_columns', None)

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_columns},
                        status=status.HTTP_200_OK)


class ChrMapViewSet(ListModelFieldsMixin,
                    CustomCreateMixin,
                    PageSizeModelMixin,
                    viewsets.ModelViewSet,
                    CountModelMixin):
    """
    ChrMapViewSet is a Django viewset for the ChrMap model. It provides a RESTful
    API for clients to interact with ChrMap objects, including creating, reading,
    updating, and deleting instances.

    Inheritance:
        ListModelFieldsMixin: Provides a mixin to list all available fields for the model.
        CustomCreateMixin: Allows for custom creation of instances.
        PageSizeModelMixin: Provides a mixin to handle pagination and page size.
        viewsets.ModelViewSet: A base class for generic model viewsets.
        CountModelMixin: Provides a mixin to return the total count of objects.

    Attributes:
        queryset: The base queryset for this viewset. Retrieves all ChrMap objects
                  and orders them by their ID.
        serializer_class: The serializer to use for handling ChrMap objects. In this
                          case, it's the ChrMapSerializer.
        permission_classes: Defines the permission classes for this viewset.
                            Allows any user to access this viewset.

    API Endpoints:
        1. List: GET /api/chrmaps/ - Retrieves a paginated list of all ChrMap objects.
        2. Create: POST /api/chrmaps/ - Creates a new ChrMap object with the provided data.
        3. Retrieve: GET /api/chrmaps/<id>/ - Retrieves a specific ChrMap object by ID.
        4. Update: PUT/PATCH /api/chrmaps/<id>/ - Updates a specific ChrMap object by ID.
        5. Delete: DELETE /api/chrmaps/<id>/ - Deletes a specific ChrMap object by ID.
    """
    queryset = ChrMap.objects.all().order_by('id')  # noqa
    serializer_class = ChrMapSerializer  # noqa
    permission_classes = (AllowAny,)


class GeneViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Gene.objects.all().order_by('id')  # noqa
    serializer_class = GeneSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = GeneFilter
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['locus_tag', 'gene']


class PromoterRegionsViewSet(ListModelFieldsMixin,
                             CustomCreateMixin,
                             PageSizeModelMixin,
                             viewsets.ModelViewSet,
                             CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PromoterRegions.objects.all().order_by('id')  # noqa
    serializer_class = PromoterRegionsSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = PromoterRegionsFilter


class HarbisonChIPViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
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

    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['tf__locus_tag', 'gene__gene']

    @action(detail=False, methods=['get'], url_path='with_annote', url_name='with-annote')
    def with_annotations(self, request, *args, **kwargs):
        annotated_queryset = HarbisonChIP.objects.with_annotations().order_by('id')

        # Apply the filtering
        filtered_queryset = self.filter_queryset(annotated_queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = HarbisonChIPAnnotatedSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HarbisonChIPAnnotatedSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='with_annote/count', url_name='with-annote-count')
    def with_annotations_count(self, request, *args, **kwargs) -> Response:
        annote_qs = HarbisonChIP.objects.with_annotations()
        annote_qs_fltr = HarbisonChIPFilter(
            self.request.GET,
            queryset=annote_qs)
        content = {'count': self.get_count(annote_qs_fltr.qs)}
        return Response(content)

    @action(detail=False, url_path='with_annote/pagination_info', url_name='with-annote-pagination-info')
    def with_annotations_pagination_info(self, request, *args, **kwargs) -> Response:
        return self.pagination_info(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='with_annote/fields', url_name='with-annote-fields')
    def with_annotation_fields(self, request, *args, **kwargs):
        # Get the _readable_fields attribute of the HarbisonChIPAnnotatedSerializer instance
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


class KemmerenTFKOViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KemmerenTFKO.objects.all().order_by('id')  # noqa
    serializer_class = KemmerenTFKOSerializer  # noqa
    permission_classes = (AllowAny,)


class McIsaacZEVViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = McIsaacZEV.objects.all().order_by('id')  # noqa
    serializer_class = McIsaacZEVSerializer  # noqa
    permission_classes = (AllowAny,)


class BackgroundViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Background.objects.all().order_by('id')  # noqa
    serializer_class = BackgroundSerializer  # noqa
    permission_classes = (AllowAny,)


class CCTFViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCTF.objects.all().order_by('id')  # noqa
    serializer_class = CCTFSerializer  # noqa
    permission_classes = (AllowAny,)


class CCExperimentViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCExperiment.objects.all().order_by('id')  # noqa
    serializer_class = CCExperimentSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = CCExperimentFilter


class HopsViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hops.objects.all().order_by('id')  # noqa
    serializer_class = HopsSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsReplicacteSigViewSet(ListModelFieldsMixin,
                               CustomCreateMixin,
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

    @action(detail=False, methods=['get'], url_path='with_annote', url_name='with-annote')
    def with_annotations(self, request, *args, **kwargs):
        annotated_queryset = HopsReplicateSig.objects.with_annotations().order_by('id')

        # Apply the filtering
        filtered_queryset = self.filter_queryset(annotated_queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = HopsReplicateSigAnnotatedSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HopsReplicateSigAnnotatedSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='with_annote/count', url_name='with-annote-count')
    def with_annotations_count(self, request, *args, **kwargs) -> Response:
        hops_with_annotations = HopsReplicateSig.objects.with_annotations()
        hops_with_annotations_fltr = HopsReplicateSigFilter(
            self.request.GET,
            queryset=hops_with_annotations)
        content = {'count': self.get_count(hops_with_annotations_fltr.qs)}
        return Response(content)

    @action(detail=False, url_path='with_annote/pagination_info', url_name='with-annote-pagination-info')
    def with_annotations_pagination_info(self, request, *args, **kwargs) -> Response:
        return self.pagination_info(request, *args, **kwargs)

    @action(detail=False, url_path='with_annote/fields', url_name='with-annote-fields')
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


class QcMetricsViewSet(ListModelFieldsMixin,
                       CustomCreateMixin,
                       PageSizeModelMixin,
                       viewsets.ModelViewSet,
                       CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcMetrics.objects.all().order_by('id')  # noqa
    serializer_class = QcMetricsSerializer  # noqa
    permission_classes = (AllowAny,)


class QcManualReviewViewSet(ListModelFieldsMixin,
                            CustomCreateMixin,
                            PageSizeModelMixin,
                            viewsets.ModelViewSet,
                            CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcManualReview.objects.all().order_by('id')  # noqa
    serializer_class = QcManualReviewSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR1ToR2ViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR1ToR2Tf.objects.all().order_by('id')  # noqa
    serializer_class = QcR1ToR2TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR2ToR1ViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR2ToR1Tf.objects.all().order_by('id')  # noqa
    serializer_class = QcR2ToR1TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcTfToTransposonViewSet(ListModelFieldsMixin,
                              CustomCreateMixin,
                              PageSizeModelMixin,
                              viewsets.ModelViewSet,
                              CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcTfToTransposon.objects.all().order_by('id')  # noqa
    serializer_class = QcTfToTransposonSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR1ToR2TfSummaryViewSet(viewsets.ViewSet):
    def list(self, request):

        r1_r2_max_tally_subquery = QcR1ToR2Tf.objects.filter(
            experiment_id=OuterRef('pk')
        ).order_by('-tally').values('edit_dist')[:1]

        r2_r1_max_tally_subquery = QcR2ToR1Tf.objects.filter(
            experiment_id=OuterRef('pk')
        ).order_by('-tally').values('edit_dist')[:1]

        query = (
            CCExperiment.objects
            .annotate(
                experiment_id=F('id'),
                r1_r2_max_tally=Max('qcr1tor2tf__tally'),
                r1_r2_status=Subquery(r1_r2_max_tally_subquery),
                r2_r1_max_tally=Max('qcr2tor1tf__tally'),
                r2_r1_status=Subquery(r2_r1_max_tally_subquery),
            )
            .filter(Q(r1_r2_max_tally__isnull=False) | Q(r2_r1_max_tally__isnull=False))
            .order_by('experiment_id')
            .values('experiment_id', 'r1_r2_status', 'r2_r1_status')
        )

        for item in query:
            item['r1_r2_status'] = 'pass' if item['r1_r2_status'] == 0 else 'fail'
            item['r2_r1_status'] = 'pass' if item['r2_r1_status'] == 0 else 'fail'

        serializer = BarcodeComponentsSummarySerializer(query, many=True)
        return Response(serializer.data)


class QcReviewViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):

    serializer_class = QcReviewSerializer

    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):

        hop_count_subquery = Hops.objects.filter(
            experiment_id=OuterRef('pk')
        ).annotate(count=Count('experiment')
                   ).values('count')

        r1_r2_max_tally_subquery = QcR1ToR2Tf.objects.filter(
            experiment_id=OuterRef('pk')
        ).order_by('-tally').values('edit_dist')[:1]

        r2_r1_max_tally_subquery = QcR2ToR1Tf.objects.filter(
            experiment_id=OuterRef('pk')
        ).order_by('-tally').values('edit_dist')[:1]

        unknown_feature_id = Gene.objects\
            .get(locus_tag=UNDETERMINED_LOCUS_TAG).id

        ccexperiment_fltr = CCExperimentFilter(self.request.GET)

        query = (
            ccexperiment_fltr.qs
            .exclude(tf_id=unknown_feature_id)
            .select_related('tf_id', 'qcmetrics', 'qcmanualreview')
            .annotate(
                experiment_id=F('id'),
                tf_alias=Case(
                    When(tf__tf__gene__istartswith='unknown',
                         then=F('tf__tf__locus_tag')),
                    default=F('tf__tf__gene'),
                    output_field=CharField()),
                r1_r2_max_tally=Max('qcr1tor2tf__tally'),
                r1_r2_status=Subquery(r1_r2_max_tally_subquery),
                r2_r1_max_tally=Max('qcr2tor1tf__tally'),
                r2_r1_status=Subquery(r2_r1_max_tally_subquery),
                map_unmap_ratio=F('qcmetrics__genome_mapped') / F('qcmetrics__unmapped'),
                num_hops=Subquery(hop_count_subquery),
                rank_recall=F('qcmanualreview__rank_recall'),
                chip_better=F('qcmanualreview__chip_better'),
                data_usable=F('qcmanualreview__data_usable'),
                passing_replicate=F('qcmanualreview__passing_replicate'),
                note=F('qcmanualreview__note')
            )
            .order_by('tf_alias', 'batch', 'batch_replicate')
            .values('experiment_id', 'tf_alias', 'batch', 'batch_replicate',
                    'r1_r2_status', 'r2_r1_status', 'map_unmap_ratio',
                    'num_hops', 'rank_recall', 'chip_better', 'data_usable',
                    'passing_replicate', 'note')
        )

        for item in query:
            item['r1_r2_status'] = 'pass' if item['r1_r2_status'] == 0 \
                else 'fail'
            item['r2_r1_status'] = 'pass' if item['r2_r1_status'] == 0 \
                else 'fail'

        return query

    def update(self, request, pk=None):
        manual_review = QcManualReview.objects.get(pk=pk)

        qc_review_combined = self.get_queryset().get(experiment_id=pk)
        qc_review_combined_data = QcReviewSerializer(qc_review_combined).data

        # Get the fields that are present in the QcManualReviewSerializer
        valid_fields = set(QcManualReviewSerializer().get_fields().keys())

        # Get the data fields to update and filter out any invalid fields
        update_data = {key: value for key, value in
                       request.data.items() if key in valid_fields}

        serializer = QcManualReviewSerializer(
            manual_review,
            data=update_data,
            partial=True)

        if serializer.is_valid():
            serializer.save()
            qc_review_combined_data.update(serializer.data)
            drop_keys_list = ['experiment', 'id']
            for key in drop_keys_list:
                qc_review_combined_data.pop(key, None)
            response = Response(qc_review_combined_data, status=201)
            response['Cache-Control'] = 'no-cache'
        else:
            response = Response({
                'error': 'Invalid data',
                'data': update_data,
                'errors': serializer.errors
            }, status=400)

        return response


class ExpressionViewSetViewSet(ListModelFieldsMixin,
                               CustomCreateMixin,
                               PageSizeModelMixin,
                               viewsets.ModelViewSet,
                               CountModelMixin):
    """
    ExpressionViewSetViewset returns gene expression data for genes
    that have both McIsaac ZEV and Kemmeren TF-KO effect values.
    """
    serializer_class = ExpressionViewSetSerializer

    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['source_expr', 'tf_expr', 'rank_expr']
    custom_filter_columns = ['tf_id', 'gene_id', 'effect',
                             'tf_locus_tag', 'tf_gene', 'target_locus_tag',
                             'target_gene']

    def get_queryset(self):

        return_fields = ['tf_id_alias', 'tf_locus_tag', 'tf_gene',
                         'target_gene_id', 'target_locus_tag', 'target_gene',
                         'effect_expr', 'p_expr', 'source_expr']

        # Get query parameters for filtering
        mcisaac_filter = McIsaacZevFilter(self.request.GET)
        kemmeren_filter = KemmerenTfkoFilter(self.request.GET)

        mcisaac_filtered_qs = mcisaac_filter.qs\
            .annotate(
                tf_id_alias=F('tf_id'),
                tf_locus_tag=F('tf_id__locus_tag'),
                tf_gene=F('tf_id__gene'),
                target_gene_id=F('gene_id'),
                target_locus_tag=F('gene_id__locus_tag'),
                target_gene=F('gene_id__gene'),
                effect_expr=F('effect'),
                p_expr=Value(0),
                source_expr=Value('mcisaac_zev'))\
            .values(*return_fields)

        kemmeren_filtered_qs = kemmeren_filter.qs\
            .annotate(
                tf_id_alias=F('tf_id'),
                tf_locus_tag=F('tf_id__locus_tag'),
                tf_gene=F('tf_id__gene'),
                target_gene_id=F('gene_id'),
                target_locus_tag=F('gene_id__locus_tag'),
                target_gene=F('gene_id__gene'),
                effect_expr=F('effect'),
                p_expr=F('padj'),
                source_expr=Value('kemmeren_tfko'))\
            .values(*return_fields)

        # Combine the two querysets and order by 'tf' and 'gene'
        concatenated_query = mcisaac_filtered_qs\
            .union(kemmeren_filtered_qs)\
            .order_by('source_expr', 'tf_id_alias')

        return concatenated_query

    @action(detail=False, methods=['get'])
    def fields(self, request, *args, **kwargs):

        # Get the _readable_fields attribute of the dummy serializer instance
        readable = ['tf_alias', 'gene_alias', 'effect_expr', 'p_expr', 'source_expr']
        writable = None
        automatically_generated = None

        try:
            filter_columns = self.filterset_class.Meta.fields
        except AttributeError:
            # Use the custom_filter_columns attribute if available
            # this needs to be set in the viewset class when there is no
            # filterset_class
            filter_columns = getattr(self, 'custom_filter_columns', None)

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_columns},
                        status=status.HTTP_200_OK)
