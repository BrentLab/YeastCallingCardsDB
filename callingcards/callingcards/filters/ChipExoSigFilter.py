import django_filters
from ..models import ChipExoSig


class ChipExoSigFilter(django_filters.FilterSet):
    regulator_locus_tag = django_filters.CharFilter(
        field_name="chipexodata_id__regulator__locus_tag",
        lookup_expr="iexact")
    regulator_gene = django_filters.CharFilter(
        field_name="chipexodata_id__regulator__gene",
        lookup_expr="iexact")
    promoterregions_source = django_filters.CharFilter(
        field_name="promoterregions_id__source__providence",
        lookup_expr="iexact")

    class Meta:
        model = ChipExoSig
        fields = ['regulator_locus_tag', 'regulator_gene',
                  'promoterregions_source']
