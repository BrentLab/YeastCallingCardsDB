from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import QcTfToTransposon
from ..serializers import QcTfToTransposonSerializer
from ..filters import QcTfToTransposonFilter


class QcTfToTransposonViewSet(ListModelFieldsMixin,
                              CustomCreateMixin,
                              CustomValidateMixin,
                              UpdateModifiedMixin,
                              PageSizeModelMixin,
                              viewsets.ModelViewSet,
                              CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcTfToTransposon.objects.all().order_by('id')  # noqa
    serializer_class = QcTfToTransposonSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = QcTfToTransposonFilter
