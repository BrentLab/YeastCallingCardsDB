import logging

from rest_framework import serializers

from .models import (ChrMap, Gene, PromoterRegions, HarbisonChIP,
                     KemmerenTFKO, McIsaacZEV, Background, CCTF,
                     CCExperiment, Hops, HopsReplicateSig, QcMetrics,
                     QcManualReview, QcR1ToR2Tf, QcR2ToR1Tf, QcTfToTransposon)

logging.getLogger(__name__).addHandler(logging.NullHandler())


class ChrMapSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = ChrMap  # noqa
        fields = '__all__'


class GeneSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = Gene  # noqa
        fields = '__all__'


class PromoterRegionsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = PromoterRegions  # noqa
        fields = '__all__'


class PromoterRegionsTargetsOnlySerializer(serializers.Serializer):
    promoter_id = serializers.IntegerField()
    target_gene_id = serializers.IntegerField()
    target_locus_tag = serializers.CharField()
    target_gene = serializers.CharField()
    source = serializers.CharField()


class PromoterHopsBackgroundViewSerializer(serializers.ModelSerializer):
    expression_hops = serializers.IntegerField()
    background_hops = serializers.IntegerField()
    effect = serializers.FloatField()

    class Meta:
        model = PromoterRegions
        fields = ('id', 'expression_hops', 'background_hops', 'effect')


class HarbisonChIPSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = HarbisonChIP  # noqa
        fields = '__all__'


class HarbisonChIPAnnotatedSerializer(serializers.Serializer):
    tf_id = serializers.IntegerField()
    tf_locus_tag = serializers.CharField()
    tf_gene = serializers.CharField()
    target_gene_id = serializers.IntegerField()
    target_locus_tag = serializers.CharField()
    target_gene = serializers.CharField()
    binding_signal = serializers.FloatField()
    experiment = serializers.CharField()


class KemmerenTFKOSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = KemmerenTFKO  # noqa
        fields = '__all__'


class McIsaacZEVSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = McIsaacZEV  # noqa
        fields = '__all__'


class BackgroundSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = Background  # noqa
        fields = '__all__'


class CCTFSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = CCTF  # noqa
        fields = '__all__'

class CCTFListSerializer(serializers.Serializer):
    tf_id = serializers.IntegerField()
    tf_locus_tag = serializers.CharField()
    tf_gene = serializers.CharField()

class CCExperimentSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = CCExperiment  # noqa
        fields = '__all__'


class HopsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = Hops  # noqa
        fields = '__all__'


class HopsReplicateSigSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = HopsReplicateSig  # noqa
        fields = '__all__'


class QcMetricsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = QcMetrics  # noqa
        fields = '__all__'

class QcManualReviewSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = QcManualReview  # noqa
        fields = '__all__'


class QcR1ToR2TfSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = QcR1ToR2Tf  # noqa
        fields = '__all__'


class QcR2ToR1TfSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = QcR2ToR1Tf  # noqa
        fields = '__all__'


class QcTfToTransposonSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(source='modifiedBy.username')

    class Meta:
        model = QcTfToTransposon  # noqa
        fields = '__all__'

class BarcodeComponentsSummarySerializer(serializers.Serializer):
    experiment_id = serializers.IntegerField()
    r1_r2_status = serializers.CharField()
    r2_r1_status = serializers.CharField()


class QcReviewSerializer(serializers.Serializer):
    experiment_id = serializers.IntegerField()
    tf_alias = serializers.CharField()
    batch = serializers.CharField()
    batch_replicate = serializers.IntegerField()
    r1_r2_max_tally_edit_dist = serializers.CharField()
    r2_r1_max_tally_edit_dist = serializers.CharField()
    map_unmap_ratio = serializers.FloatField()
    num_hops = serializers.IntegerField()
    rank_recall = serializers.CharField()
    chip_better = serializers.CharField()
    data_usable = serializers.CharField()
    passing_replicate = serializers.CharField()
    note = serializers.CharField()

class ExpressionViewSetSerializer(serializers.Serializer):
    tf_id_alias = serializers.IntegerField()
    tf_locus_tag = serializers.CharField()
    tf_gene = serializers.CharField()
    target_gene_id = serializers.IntegerField()
    target_locus_tag = serializers.CharField()
    target_gene = serializers.CharField()
    effect_expr = serializers.FloatField()
    p_expr = serializers.FloatField()
    source_expr = serializers.CharField()


class HopsReplicateSigAnnotatedSerializer(serializers.Serializer):
    tf_id_alias = serializers.IntegerField()
    tf_locus_tag = serializers.CharField()
    tf_gene = serializers.CharField()
    target_gene_id = serializers.IntegerField()
    target_locus_tag = serializers.CharField()
    target_gene = serializers.CharField()
    bg_hops = serializers.IntegerField()
    expr_hops = serializers.IntegerField()
    poisson_pval = serializers.FloatField()
    hypergeom_pval = serializers.FloatField()
    experiment = serializers.IntegerField()
    experiment_batch = serializers.CharField()
    experiment_batch_replicate = serializers.IntegerField()
    background = serializers.CharField()
    promoter_id = serializers.IntegerField()
    promoter_source = serializers.CharField()
