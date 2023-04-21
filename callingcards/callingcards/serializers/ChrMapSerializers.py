import logging

from rest_framework import serializers

from ..models import (ChrMap)

logging.getLogger(__name__)


class ChrMapSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = ChrMap  # noqa
        fields = '__all__'

