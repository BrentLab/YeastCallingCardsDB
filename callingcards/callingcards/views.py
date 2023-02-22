import logging

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['ChrMapViewSet', 'GeneViewSet', 'PromoterRegionsViewSet',
           'HarbisonChIPViewSet', 'KemmerenTFKOViewSet', 'McIsaacZEVViewSet',
           'BackgroundViewSet', 'CCTFViewSet', 'CCExperimentViewSet',
           'HopsViewSet', 'HopsRepliacteSigViewSet', 'QcAlignmentViewSet',
           'QcHopsViewSet', 'QcManualReviewViewSet', 'QcR1ToR2ViewSet',
           'QcR2ToR1ViewSet', 'QcTfToTransposonViewSet']


class ChrMapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChrMap.objects.all()  # noqa
    serializer_class = ChrMapSerializer  # noqa
    permission_classes = (AllowAny,)


class GeneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Gene.objects.all()  # noqa
    serializer_class = GeneSerializer  # noqa
    permission_classes = (AllowAny,)


class PromoterRegionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PromoterRegions.objects.all()  # noqa
    serializer_class = PromoterRegionsSerializer  # noqa
    permission_classes = (AllowAny,)


class HarbisonChIPViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HarbisonChIP.objects.all()  # noqa
    serializer_class = HarbisonChIPSerializer  # noqa
    permission_classes = (AllowAny,)


class KemmerenTFKOViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KemmerenTFKO.objects.all()  # noqa
    serializer_class = KemmerenTFKOSerializer  # noqa
    permission_classes = (AllowAny,)


class McIsaacZEVViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = McIsaacZEV.objects.all()  # noqa
    serializer_class = McIsaacZEVSerailizer  # noqa
    permission_classes = (AllowAny,)


class BackgroundViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Background.objects.all()  # noqa
    serializer_class = BackgroundSerializer  # noqa
    permission_classes = (AllowAny,)


class CCTFViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCTF.objects.all()  # noqa
    serializer_class = CCTFSerializer  # noqa
    permission_classes = (AllowAny,)


class CCExperimentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCExperiment.objects.all()  # noqa
    serializer_class = CCExperimentSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hops.objects.all()  # noqa
    serializer_class = HopsSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsRepliacteSigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HopsReplicateSig.objects.all()  # noqa
    serializer_class = HopsReplicateSigSerializer  # noqa
    permission_classes = (AllowAny,)


class QcAlignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcAlignment.objects.all()  # noqa
    serializer_class = QcAlignmentSerializer  # noqa
    permission_classes = (AllowAny,)


class QcHopsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcHops.objects.all()  # noqa
    serializer_class = QcHopsSerializer  # noqa
    permission_classes = (AllowAny,)


class QcManualReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcManualReview.objects.all()  # noqa
    serializer_class = QcManualReviewSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR1ToR2ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR1ToR2Tf.objects.all()  # noqa
    serializer_class = QcR1ToR2TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR2ToR1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR2ToR1Tf.objects.all()  # noqa
    serializer_class = QcR2ToR1TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcTfToTransposonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcTfToTransposon.objects.all()  # noqa
    serializer_class = QcTfToTransposonSerializer  # noqa
    permission_classes = (AllowAny,)
