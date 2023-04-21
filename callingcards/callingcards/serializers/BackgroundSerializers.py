import logging

from rest_framework import serializers

from ..models import Background

logging.getLogger(__name__)


class BackgroundSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = Background  # noqa
        fields = '__all__'
