# pylint: disable=W1203
import logging
from rest_framework import viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import (CustomCreateMixin,
                     PageSizeModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import Regulator
from ..serializers import (RegulatorSerializer,)
from ..filters import RegulatorFilter


logger = logging.getLogger(__name__)


class RegulatorViewSet(CustomCreateMixin,
                       CustomValidateMixin,
                       UpdateModifiedMixin,
                       PageSizeModelMixin,
                       viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Regulator.objects.all().order_by('id')
    serializer_class = RegulatorSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = RegulatorFilter
    search_fields = ('regulator__locus_tag', 'regulator__gene')
