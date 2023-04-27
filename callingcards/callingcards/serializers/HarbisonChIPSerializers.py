import logging

from rest_framework import serializers

from ..models import HarbisonChIP

logging.getLogger(__name__)


<<<<<<< HEAD

=======
>>>>>>> 419f5fae9547a0b963b8cd27cadfb475b0f264ca
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

