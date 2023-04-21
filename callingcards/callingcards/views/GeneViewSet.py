from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import Gene
from ..serializers import GeneSerializer
from ..filters import GeneFilter


class GeneViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  CustomValidateMixin,
                  UpdateModifiedMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Gene.objects.all().order_by('id')
    serializer_class = GeneSerializer
    permission_classes = (AllowAny,)

    filterset_class = GeneFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['locus_tag', 'gene']
