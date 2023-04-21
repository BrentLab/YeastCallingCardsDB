from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin, CustomCreateMixin, 
                     UpdateModifiedMixin, PageSizeModelMixin, 
                     CountModelMixin,
                     CustomValidateMixin)
from ..models import Background
from ..serializers import BackgroundSerializer


class BackgroundViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        UpdateModifiedMixin,
                        CustomValidateMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Background.objects.all().order_by('id')  # noqa
    serializer_class = BackgroundSerializer  # noqa
    permission_classes = (AllowAny,)
