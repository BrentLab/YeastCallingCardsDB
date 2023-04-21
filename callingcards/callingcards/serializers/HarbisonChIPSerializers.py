import logging

from rest_framework import serializers

from ..models import HarbisonChIP

logging.getLogger(__name__)



class HarbisonChIPSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

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

