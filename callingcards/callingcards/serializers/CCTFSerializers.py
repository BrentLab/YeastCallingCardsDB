import logging

from rest_framework import serializers

from ..models import (CCTF)

logging.getLogger(__name__)


class CCTFSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = CCTF  # noqa
        fields = '__all__'

class CCTFListSerializer(serializers.Serializer):
    tf_id = serializers.IntegerField()
    tf_locus_tag = serializers.CharField()
    tf_gene = serializers.CharField()
