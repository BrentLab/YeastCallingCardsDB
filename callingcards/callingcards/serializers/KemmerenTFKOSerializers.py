import logging

from rest_framework import serializers

from ..models import KemmerenTFKO

logging.getLogger(__name__)


class KemmerenTFKOSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = KemmerenTFKO  # noqa
        fields = '__all__'
