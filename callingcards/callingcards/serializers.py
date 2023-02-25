import logging

from rest_framework import serializers

from .models import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['ChrMapSerializer', 'GeneSerializer', 'PromoterRegionsSerializer',
           'HarbisonChIPSerializer', 'KemmerenTFKOSerializer',
           'McIsaacZEVSerializer', 'BackgroundSerializer',
           'CCTFSerializer', 'CCExperimentSerializer', 'HopsSerializer',
           'HopsReplicateSigSerializer', 'QcMetricsSerializer',
           'QcManualReviewSerializer',
           'QcR1ToR2TfSerializer', 'QcR2ToR1TfSerializer',
           'QcTfToTransposonSerializer']


class ChrMapSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = ChrMap  # noqa
        fields = '__all__'


class GeneSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = Gene  # noqa
        fields = '__all__'


class PromoterRegionsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = PromoterRegions  # noqa
        fields = '__all__'


class HarbisonChIPSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = HarbisonChIP  # noqa
        fields = '__all__'


class KemmerenTFKOSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = KemmerenTFKO  # noqa
        fields = '__all__'


class McIsaacZEVSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = McIsaacZEV  # noqa
        fields = '__all__'


class BackgroundSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = Background  # noqa
        fields = '__all__'


class CCTFSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = CCTF  # noqa
        fields = '__all__'


class CCExperimentSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = CCExperiment  # noqa
        fields = '__all__'


class HopsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = Hops  # noqa
        fields = '__all__'


class HopsReplicateSigSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = HopsReplicateSig  # noqa
        fields = '__all__'


class QcMetricsSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = QcMetrics  # noqa
        fields = '__all__'

class QcManualReviewSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = QcManualReview  # noqa
        fields = '__all__'


class QcR1ToR2TfSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = QcR1ToR2Tf  # noqa
        fields = '__all__'


class QcR2ToR1TfSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = QcR2ToR1Tf  # noqa
        fields = '__all__'


class QcTfToTransposonSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = QcTfToTransposon  # noqa
        fields = '__all__'
