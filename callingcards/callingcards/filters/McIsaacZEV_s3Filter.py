import django_filters
from ..models import McIsaacZEV_s3


class McIsaacZEV_s3Filter(django_filters.FilterSet):
    tf_locus_tag = django_filters.CharFilter(
        field_name="tf_id__locus_tag",
        lookup_expr="iexact")
    tf_gene = django_filters.CharFilter(
        field_name="tf_id__gene",
        lookup_expr="iexact")
    time = django_filters.CharFilter(
        field_name="time",
        lookup_expr="iexact")

    class Meta:
        model = McIsaacZEV_s3
        fields = ['tf_locus_tag', 'tf_gene', 'time']
