import logging

from rest_framework import serializers

from ..models import Hu_s3

logging.getLogger(__name__)


class Hu_s3Serializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = Hu_s3  # noqa
        fields = '__all__'
