import logging

from rest_framework import serializers

from ..models import ChipExoSig

logging.getLogger(__name__)


class ChipExoSigSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = ChipExoSig  # noqa
        fields = '__all__'
