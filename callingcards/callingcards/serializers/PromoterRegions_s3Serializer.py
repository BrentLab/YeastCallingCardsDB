import logging

from rest_framework import serializers

from ..models import PromoterRegions_s3

logging.getLogger(__name__)


class PromoterRegions_s3Serializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = PromoterRegions_s3  # noqa
        fields = '__all__'
