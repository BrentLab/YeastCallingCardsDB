import logging

from rest_framework import serializers

from ..models import PromoterRegions

logging.getLogger(__name__)


class PromoterRegionsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

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

