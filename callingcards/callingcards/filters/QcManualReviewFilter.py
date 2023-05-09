import django_filters
from ..models import QcManualReview


class QcManualReviewFilter(django_filters.FilterSet):

    class Meta:
        model = QcManualReview
        fields = "__all__"
