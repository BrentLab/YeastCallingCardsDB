import logging

from rest_framework import serializers

from ..models import HopsSource

logging.getLogger(__name__)


class HopsSourceSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = HopsSource  # noqa
        fields = '__all__'

