import django_filters
from ..models import ChipExo_s3


class ChipExo_s3Filter(django_filters.FilterSet):
    tf_locus_tag = django_filters.CharFilter(
        field_name="tf__locus_tag",
        lookup_expr="iexact")
    tf_gene = django_filters.CharFilter(
        field_name="tf__gene",
        lookup_expr="iexact")

    class Meta:
        model = ChipExo_s3
        fields = ['tf_locus_tag', 'tf_gene']
