from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import QcR1ToR2Tf
from ..serializers import QcR1ToR2TfSerializer
from ..filters import QcR1ToR2TfFilter


class QcR1ToR2ViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      CustomValidateMixin,
                      UpdateModifiedMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR1ToR2Tf.objects.all().order_by('id')  # noqa
    serializer_class = QcR1ToR2TfSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = QcR1ToR2TfFilter
