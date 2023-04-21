import logging

from rest_framework import serializers

from ..models import (CCExperiment)

logging.getLogger(__name__)


class CCExperimentSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = CCExperiment  # noqa
        fields = '__all__'

