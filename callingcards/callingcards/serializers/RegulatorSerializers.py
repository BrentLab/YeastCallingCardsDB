import logging

from rest_framework import serializers

from ..models import (Regulator)

logging.getLogger(__name__)


class RegulatorSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    modifiedBy = serializers.CharField(
        source='uploader.username',
        required=False)

    class Meta:
        model = Regulator  # noqa
        fields = '__all__'


class RegulatorListSerializer(serializers.Serializer):
    regulator_id = serializers.IntegerField()
    regulator_locus_tag = serializers.CharField()
    regulator_gene = serializers.CharField()
