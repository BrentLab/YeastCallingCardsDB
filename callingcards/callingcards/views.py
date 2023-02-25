import logging

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['ChrMapViewSet', 'GeneViewSet', 'PromoterRegionsViewSet',
           'HarbisonChIPViewSet', 'KemmerenTFKOViewSet', 'McIsaacZEVViewSet',
           'BackgroundViewSet', 'CCTFViewSet', 'CCExperimentViewSet',
           'HopsViewSet', 'HopsReplicacteSigViewSet', 'QcMetricsViewSet',
           'QcManualReviewViewSet', 'QcR1ToR2ViewSet',
           'QcR2ToR1ViewSet', 'QcTfToTransposonViewSet']

class UserCreateMixin:
    """
    By default the user field is "user" you can change it
    to your model "user" field.
    cite: https://xploit29.com/2016/09/15/django-rest-framework-auto-assign-current-user-on-creation/

    Usage:
    class PostViewSet(UserCreateMixin, viewsets.ModelViewSet):
        # ViewsSet required info...
        user_field = 'creator'
    """

    _user_field = None

    @property
    def user_field(self):
        """user field is the field from the model that will be set to the current user.
        defaults to "uploder" """
        return self._user_field or 'uploader'

    @user_field.setter
    def user_field(self, value):
        self._user_field = value

    def perform_create(self, serializer):
        """set the user field to the current user
            args:
                serializer: the serializer that will be used to save the model
        """
        kwargs = {
            self.user_field: self.request.user
        }

        serializer.save(**kwargs)

        super().perform_create(serializer)


class ChrMapViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChrMap.objects.all()  # noqa
    serializer_class = ChrMapSerializer  # noqa
    permission_classes = (AllowAny,)

    # def perform_create(self, **kwargs):
    #     super().perform_create(**kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(uploader=self.request.user)


class GeneViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Gene.objects.all()  # noqa
    serializer_class = GeneSerializer  # noqa
    permission_classes = (AllowAny,)


class PromoterRegionsViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PromoterRegions.objects.all()  # noqa
    serializer_class = PromoterRegionsSerializer  # noqa
    permission_classes = (AllowAny,)


class HarbisonChIPViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HarbisonChIP.objects.all()  # noqa
    serializer_class = HarbisonChIPSerializer  # noqa
    permission_classes = (AllowAny,)


class KemmerenTFKOViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KemmerenTFKO.objects.all()  # noqa
    serializer_class = KemmerenTFKOSerializer  # noqa
    permission_classes = (AllowAny,)


class McIsaacZEVViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = McIsaacZEV.objects.all()  # noqa
    serializer_class = McIsaacZEVSerializer  # noqa
    permission_classes = (AllowAny,)


class BackgroundViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Background.objects.all()  # noqa
    serializer_class = BackgroundSerializer  # noqa
    permission_classes = (AllowAny,)


class CCTFViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCTF.objects.all()  # noqa
    serializer_class = CCTFSerializer  # noqa
    permission_classes = (AllowAny,)


class CCExperimentViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCExperiment.objects.all()  # noqa
    serializer_class = CCExperimentSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hops.objects.all()  # noqa
    serializer_class = HopsSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsReplicacteSigViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HopsReplicateSig.objects.all()  # noqa
    serializer_class = HopsReplicateSigSerializer  # noqa
    permission_classes = (AllowAny,)


class QcMetricsViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcMetrics.objects.all()  # noqa
    serializer_class = QcMetricsSerializer  # noqa
    permission_classes = (AllowAny,)


class QcManualReviewViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcManualReview.objects.all()  # noqa
    serializer_class = QcManualReviewSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR1ToR2ViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR1ToR2Tf.objects.all()  # noqa
    serializer_class = QcR1ToR2TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR2ToR1ViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR2ToR1Tf.objects.all()  # noqa
    serializer_class = QcR2ToR1TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcTfToTransposonViewSet(UserCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcTfToTransposon.objects.all()  # noqa
    serializer_class = QcTfToTransposonSerializer  # noqa
    permission_classes = (AllowAny,)
