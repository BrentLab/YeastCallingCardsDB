import logging

from rest_framework import serializers

from ..models import (QcMetrics,
                     QcManualReview,
                     QcR1ToR2Tf,
                     QcR2ToR1Tf,
                     QcTfToTransposon)

logging.getLogger(__name__)



class BarcodeComponentsSummarySerializer(serializers.Serializer):
    experiment_id = serializers.IntegerField()
    r1_r2_status = serializers.CharField()
    r2_r1_status = serializers.CharField()

class QcMetricsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = QcMetrics  # noqa
        fields = '__all__'

class QcManualReviewSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = QcManualReview  # noqa
        fields = '__all__'


class QcR1ToR2TfSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = QcR1ToR2Tf  # noqa
        fields = '__all__'


class QcR2ToR1TfSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = QcR2ToR1Tf  # noqa
        fields = '__all__'


class QcReviewSerializer(serializers.Serializer):
    experiment_id = serializers.IntegerField()
    tf_alias = serializers.CharField()
    batch = serializers.CharField()
    batch_replicate = serializers.IntegerField()
    r1_r2_max_tally_edit_dist = serializers.CharField()
    r2_r1_max_tally_edit_dist = serializers.CharField()
    map_unmap_ratio = serializers.FloatField()
    genomic_hops = serializers.IntegerField()
    mito_hops = serializers.IntegerField()
    plasmid_hops = serializers.IntegerField()
    rank_recall = serializers.CharField()
    chip_better = serializers.CharField()
    data_usable = serializers.CharField()
    passing_replicate = serializers.CharField()
    note = serializers.CharField()


class QcTfToTransposonSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = QcTfToTransposon  # noqa
        fields = '__all__'

