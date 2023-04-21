from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import QcR2ToR1Tf
from ..serializers import QcR2ToR1TfSerializer
from ..filters import QcR2ToR1TfFilter


class QcR2ToR1ViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      CustomValidateMixin,
                      UpdateModifiedMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR2ToR1Tf.objects.all().order_by('id')  # noqa
    serializer_class = QcR2ToR1TfSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = QcR2ToR1TfFilter
