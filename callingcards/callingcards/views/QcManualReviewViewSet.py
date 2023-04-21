from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import QcManualReview
from ..serializers import QcManualReviewSerializer
from ..filters import QcManualReviewFilter


class QcManualReviewViewSet(ListModelFieldsMixin,
                            CustomCreateMixin,
                            CustomValidateMixin,
                            UpdateModifiedMixin,
                            PageSizeModelMixin,
                            viewsets.ModelViewSet,
                            CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcManualReview.objects.all().order_by('id')  # noqa
    serializer_class = QcManualReviewSerializer  # noqa
    permission_classes = (AllowAny,)
    filterset_class = QcManualReviewFilter
