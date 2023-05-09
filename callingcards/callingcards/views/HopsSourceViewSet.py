from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import HopsSource
from ..serializers import HopsSourceSerializer
from ..filters import HopsSourceFilter


class HopsSourceViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        CustomValidateMixin,
                        UpdateModifiedMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HopsSource.objects.all().order_by('source')  # noqa
    serializer_class = HopsSourceSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = HopsSourceFilter
