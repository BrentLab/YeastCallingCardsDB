import django_filters
from ..models import QcR1ToR2Tf


class QcR1ToR2TfFilter(django_filters.FilterSet):

    class Meta:
        model = QcR1ToR2Tf
        fields = "__all__"
