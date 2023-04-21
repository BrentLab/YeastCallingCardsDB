import logging

from rest_framework import serializers

logging.getLogger(__name__)


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

