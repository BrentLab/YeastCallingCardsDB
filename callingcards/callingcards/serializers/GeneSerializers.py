import logging

from rest_framework import serializers

from ..models import Gene

logging.getLogger(__name__)


class GeneSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = Gene  # noqa
        fields = '__all__'

