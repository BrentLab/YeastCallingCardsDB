import logging

from rest_framework import serializers

from ..models import McIsaacZEV

logging.getLogger(__name__)


class McIsaacZEVSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = McIsaacZEV  # noqa
        fields = '__all__'

