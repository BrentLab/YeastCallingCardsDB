import logging

from rest_framework import serializers

from ..models import HarbisonChIP_s3

logging.getLogger(__name__)


class HarbisonChIP_s3Serializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = HarbisonChIP_s3  # noqa
        fields = '__all__'
