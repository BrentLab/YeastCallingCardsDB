import django_filters
from ..models import KemmerenTFKO_s3


class KemmerenTfko_s3Filter(django_filters.FilterSet):
    regulator_locus_tag = django_filters.CharFilter(
        field_name="regulator__locus_tag",
        lookup_expr="iexact")
    regulator_gene = django_filters.CharFilter(
        field_name="regulator__gene",
        lookup_expr="iexact")

    class Meta:
        model = KemmerenTFKO_s3
        fields = ['regulator_locus_tag', 'regulator_gene']
