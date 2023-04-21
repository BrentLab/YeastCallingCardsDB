import logging

from rest_framework import serializers

from ..models import Hops

logging.getLogger(__name__)


class HopsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = Hops  # noqa
        fields = '__all__'

