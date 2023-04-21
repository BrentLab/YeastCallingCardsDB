from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import QcMetrics
from ..serializers import QcMetricsSerializer
from ..filters import QcMetricsFilter

class QcMetricsViewSet(ListModelFieldsMixin,
                       CustomCreateMixin,
                       CustomValidateMixin,
                       UpdateModifiedMixin,
                       PageSizeModelMixin,
                       viewsets.ModelViewSet,
                       CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcMetrics.objects.all().order_by('id')  # noqa
    serializer_class = QcMetricsSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = QcMetricsFilter
