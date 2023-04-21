from django.db.models import F, Max, OuterRef, Q, Subquery
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import CCExperiment, QcR1ToR2Tf, QcR2ToR1Tf
from ..serializers import BarcodeComponentsSummarySerializer


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
            .filter(Q(r1_r2_max_tally__isnull=False)
                    | Q(r2_r1_max_tally__isnull=False))
            .order_by('experiment_id')
            .values('experiment_id', 'r1_r2_status', 'r2_r1_status')
        )

        for item in query:
            item['r1_r2_status'] = 'pass' if \
                item['r1_r2_status'] == 0 else 'fail'
            item['r2_r1_status'] = 'pass' if \
                item['r2_r1_status'] == 0 else 'fail'

        serializer = BarcodeComponentsSummarySerializer(query, many=True)
        return Response(serializer.data)
