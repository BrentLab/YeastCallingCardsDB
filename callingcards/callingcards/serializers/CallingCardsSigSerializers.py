import logging

from rest_framework import serializers

from ..models import CallingCardsSig

logging.getLogger(__name__)


class CallingCardsSigSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = CallingCardsSig  # noqa
        fields = '__all__'

