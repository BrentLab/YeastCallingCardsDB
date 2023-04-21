from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import KemmerenTFKO
from ..serializers import KemmerenTFKOSerializer
from ..filters import KemmerenTfkoFilter

class KemmerenTFKOViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          CustomValidateMixin,
                          UpdateModifiedMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KemmerenTFKO.objects.all().order_by('id')  # noqa
    serializer_class = KemmerenTFKOSerializer  # noqa
    permission_classes = (AllowAny,)

    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['tf__locus_tag', 'tf__gene',
                     'gene__locus_tag', 'gene__gene']

    filterset_class = KemmerenTfkoFilter
