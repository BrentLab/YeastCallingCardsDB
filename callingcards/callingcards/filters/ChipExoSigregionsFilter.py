import django_filters
from ..models import ChipExo_s3


class ChipExoSigFilter(django_filters.FilterSet):
    tf_locus_tag = django_filters.CharFilter(
        field_name="chipexodata_id__tf__locus_tag",
        lookup_expr="iexact")
    tf_gene = django_filters.CharFilter(
        field_name="chipexodata_id__tf__gene",
        lookup_expr="iexact")
    promoterregions_source = django_filters.CharFilter(
        field_name="promoterregions_id__source__providence",
        lookup_expr="iexact")

    class Meta:
        model = ChipExo_s3
        fields = ['tf_locus_tag', 'tf_gene', 'promoterregions_source']
