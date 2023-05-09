import django_filters
from ..models import QcTfToTransposon


class QcTfToTransposonFilter(django_filters.FilterSet):

    class Meta:
        model = QcTfToTransposon
        fields = "__all__"
