import django_filters
from ..models import ChipExo


class ChipExoFilter(django_filters.FilterSet):
    tf_id = django_filters.NumberFilter(
        field_name="tf_id",
        lookup_expr="exact")
    tf_locus_tag = django_filters.CharFilter(
        field_name="tf_id__locus_tag",
        lookup_expr="iexact")
    tf_gene = django_filters.CharFilter(
        field_name="tf_id__gene",
        lookup_expr="iexact")
    target_locus_tag = django_filters.CharFilter(
        field_name="gene_id__locus_tag",
        lookup_expr="iexact")
    target_gene = django_filters.CharFilter(
        field_name="gene_id__gene",
        lookup_expr="iexact")

    class Meta:
        model = ChipExo
        fields = ['tf_id', 'tf_locus_tag', 'tf_gene',
                  'target_locus_tag', 'target_gene']
