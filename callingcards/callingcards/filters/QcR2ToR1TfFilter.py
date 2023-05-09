import django_filters
from ..models.mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin
from ..models import QcR2ToR1Tf


class QcR2ToR1TfFilter(django_filters.FilterSet):

    class Meta:
        model = QcR2ToR1Tf
        fields = "__all__"
