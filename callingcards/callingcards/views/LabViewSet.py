from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import Lab
from ..serializers import LabSerializer
from ..filters import LabFilter


class LabViewSet(ListModelFieldsMixin,
                 CustomCreateMixin,
                 CustomValidateMixin,
                 UpdateModifiedMixin,
                 PageSizeModelMixin,
                 viewsets.ModelViewSet,
                 CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lab.objects.all().order_by('lab')  # noqa
    serializer_class = LabSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = LabFilter
