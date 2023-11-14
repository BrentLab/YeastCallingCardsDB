import django_filters
from ..models import PromoterRegions_s3


class PromoterRegions_s3Filter(django_filters.FilterSet):
    source = django_filters.CharFilter(
        field_name="source",
        lookup_expr="iexact")

    class Meta:
        model = PromoterRegions_s3
        fields = ['tf_locus_tag', 'tf_gene']
