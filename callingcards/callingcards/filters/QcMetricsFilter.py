import django_filters
from ..models import QcMetrics


class QcMetricsFilter(django_filters.FilterSet):

    class Meta:
        model = QcMetrics
        fields = "__all__"
