from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import CCExperiment
from ..serializers import CCExperimentSerializer
from ..filters import CCExperimentFilter


class CCExperimentViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          CustomValidateMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin,
                          UpdateModifiedMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCExperiment.objects.all().order_by('id')  # noqa
    serializer_class = CCExperimentSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = CCExperimentFilter
