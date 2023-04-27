from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import CallingCardsSig
from ..serializers import CallingCardsSigSerializer
from ..filters import CallingCardsSigFilter


class CallingCardsSigViewSet(ListModelFieldsMixin,
                             CustomCreateMixin,
                             CustomValidateMixin,
                             PageSizeModelMixin,
                             viewsets.ModelViewSet,
                             CountModelMixin,
                             UpdateModifiedMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CallingCardsSig.objects.all().order_by('id')  # noqa
    serializer_class = CallingCardsSigSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = CallingCardsSigFilter
