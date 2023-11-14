import logging

from rest_framework import serializers

from ..models import ChipExo_s3

logging.getLogger(__name__)


class ChipExo_s3Serializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = ChipExo_s3  # noqa
        fields = '__all__'
