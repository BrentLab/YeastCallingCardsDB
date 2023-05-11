import django_filters
from ..models import Lab


class LabFilter(django_filters.FilterSet):

    class Meta:
        model = Lab
        fields = "__all__"
