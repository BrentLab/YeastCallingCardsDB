import django_filters
from ..models import ChipExo_s3


class ChipExo_s3Filter(django_filters.FilterSet):
    regulator_locus_tag = django_filters.CharFilter(
        field_name="regulator__regulator__locus_tag",
        lookup_expr="iexact")
    regulator_gene = django_filters.CharFilter(
        field_name="regulator__regulator__gene",
        lookup_expr="iexact")
    chipexo_id = django_filters.CharFilter(
        field_name="chipexo_id",
        lookup_expr="iexact")
    replicate = django_filters.NumberFilter(
        field_name="replicate",
        lookup_expr="iexact")
    condition = django_filters.CharFilter(
        field_name="condition",
        lookup_expr="iexact")
    parent_condition = django_filters.CharFilter(
        field_name="parent_condition",
        lookup_expr="iexact")
    

    class Meta:
        model = ChipExo_s3
        fields = ['regulator_locus_tag', 
                  'regulator_gene',
                  'chipexo_id',
                  'replicate',
                  'condition',
                  'parent_condition']
