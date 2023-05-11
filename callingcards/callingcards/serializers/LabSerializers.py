import logging

from rest_framework import serializers

from ..models import Lab

logging.getLogger(__name__)


class LabSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = Lab  # noqa
        fields = '__all__'