import logging

from rest_framework import serializers

from ..models import HopsReplicateSig

logging.getLogger(__name__)


class HopsReplicateSigSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = HopsReplicateSig  # noqa
        fields = '__all__'


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
