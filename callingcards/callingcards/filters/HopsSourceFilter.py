import django_filters
from ..models import HopsSource


class HopsSourceFilter(django_filters.FilterSet):

    class Meta:
        model = HopsSource
        fields = "__all__"
