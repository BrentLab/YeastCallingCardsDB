import logging

from rest_framework import serializers

from ..models import ChipExo

logging.getLogger(__name__)


class ChipExoSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = ChipExo  # noqa
        fields = '__all__'


class ChipExoAnnotatedSerializer(serializers.Serializer):
    tf_id = serializers.IntegerField()
    tf_locus_tag = serializers.CharField()
    tf_gene = serializers.CharField()
    target_gene_id = serializers.IntegerField()
    target_locus_tag = serializers.CharField()
    target_gene = serializers.CharField()
    binding_signal = serializers.FloatField()
    experiment = serializers.CharField()

