from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import Hops
from ..serializers import HopsSerializer


class HopsViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  CustomValidateMixin,
                  UpdateModifiedMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hops.objects.all().order_by('id')  # noqa
    serializer_class = HopsSerializer  # noqa
    permission_classes = (AllowAny,)
