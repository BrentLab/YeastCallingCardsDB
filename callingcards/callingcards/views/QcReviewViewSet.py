from django.db.models import (Count, Case, When, F, Value,
                              CharField, OuterRef, Subquery)
from django.db.models.functions import Coalesce, NullIf
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.response import Response
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from .constants import UNDETERMINED_LOCUS_TAG
from ..models import Hops, QcR1ToR2Tf, QcR2ToR1Tf, Gene, QcManualReview
from ..serializers import QcReviewSerializer, QcManualReviewSerializer
from ..filters import CCExperimentFilter


class QcReviewViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      CustomValidateMixin,
                      UpdateModifiedMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):

    serializer_class = QcReviewSerializer

    filter_backends = [filters.DjangoFilterBackend]

    filterset_class = CCExperimentFilter

    def get_queryset(self):

        hop_count_subquery = Hops.objects\
            .filter(experiment_id=OuterRef('pk'))\
            .values('experiment_id')\
            .annotate(count=Count('experiment_id'))\
            .values('count')

        r1_r2_max_tally_edit_dist_subquery = QcR1ToR2Tf.objects.filter(
            experiment_id=OuterRef('pk')
        ).order_by('-tally').values('edit_dist')[:1]

        r2_r1_max_tally_edit_dist_subquery = QcR2ToR1Tf.objects.filter(
            experiment_id=OuterRef('pk')
        ).order_by('-tally').values('edit_dist')[:1]

        unknown_feature_id = Gene.objects\
            .get(locus_tag=UNDETERMINED_LOCUS_TAG).id

        ccexperiment_fltr = CCExperimentFilter(self.request.GET)

        # TODO add select/prefetch related to reduce the number of queries
        # note when teh qc_metrics unmapped is 0, set to 0 to avoid divide by
        # 0 error
        query = (
            ccexperiment_fltr.qs
            .exclude(tf_id=unknown_feature_id)
            .annotate(
                experiment_id=F('id'),
                tf_alias=Case(
                    When(tf__tf__gene__istartswith='unknown',
                            then=F('tf__tf__locus_tag')),
                    default=F('tf__tf__gene'),
                    output_field=CharField()),
                r1_r2_max_tally_edit_dist=Subquery(r1_r2_max_tally_edit_dist_subquery),  # noqa
                r2_r1_max_tally_edit_dist=Subquery(r2_r1_max_tally_edit_dist_subquery),  # noqa
                map_unmap_ratio=Coalesce(
                    F('qcmetrics__genome_mapped') / NullIf(
                        F('qcmetrics__unmapped'), 0), Value(0)
                ),
                num_hops=Subquery(hop_count_subquery),
                rank_recall=F('qcmanualreview__rank_recall'),
                chip_better=F('qcmanualreview__chip_better'),
                data_usable=F('qcmanualreview__data_usable'),
                passing_replicate=F('qcmanualreview__passing_replicate'),
                note=F('qcmanualreview__note')
            )
            .order_by('tf_alias', 'batch', 'batch_replicate')
            .values('experiment_id', 'tf_alias', 'batch', 'batch_replicate',
                    'r1_r2_max_tally_edit_dist', 'r2_r1_max_tally_edit_dist',
                    'map_unmap_ratio', 'num_hops', 'rank_recall',
                    'chip_better', 'data_usable', 'passing_replicate', 'note')
        )

        # for item in query:
        #     item['r1_r2_status'] = 'pass' if item['r1_r2_status'] == 0 \
        #         else 'fail'
        #     item['r2_r1_status'] = 'pass' if item['r2_r1_status'] == 0 \
        #         else 'fail'

        return query

    def update(self, request, pk=None):

        manual_review = QcManualReview.objects.get(pk=pk)

        qc_review_combined = self.get_queryset().get(experiment_id=pk)
        qc_review_combined_data = QcReviewSerializer(qc_review_combined).data

        # Get the fields that are present in the QcManualReviewSerializer
        valid_fields = set(QcManualReviewSerializer().get_fields().keys())

        # Get the data fields to update and filter out any invalid fields
        # TODO this expects a single dict, not a list. Should it accept a list?
        # unlisting and extracting the first item is what the [0] is doing
        update_data = {key: value for key, value in
                       request.data[0].items() if key in valid_fields}

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
