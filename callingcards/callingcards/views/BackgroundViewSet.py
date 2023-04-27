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
<<<<<<< HEAD
    queryset = Background.objects.all().order_by('id')  # noqa
=======
    queryset = Background.objects.all().order_by('pk')  # noqa
>>>>>>> 419f5fae9547a0b963b8cd27cadfb475b0f264ca
    serializer_class = BackgroundSerializer  # noqa
    permission_classes = (AllowAny,)
