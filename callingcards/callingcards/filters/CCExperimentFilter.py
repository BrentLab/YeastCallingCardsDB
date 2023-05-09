import django_filters
from ..models import CCExperiment


class CCExperimentFilter(django_filters.FilterSet):
    experiment = django_filters.NumberFilter(
        field_name="id",
        lookup_expr="exact")
    experiment_id = django_filters.NumberFilter(
        field_name='id',
        lookup_expr='exact'
    )
    batch = django_filters.CharFilter(
        field_name="batch",
        lookup_expr="iexact")
    batch_replicate = django_filters.CharFilter(
        field_name="batch_replicate",
        lookup_expr="iexact")
    tf_id = django_filters.NumberFilter(
        field_name="tf__tf",
        lookup_expr="exact")
    tf_locus_tag = django_filters.CharFilter(
        field_name="tf__tf__locus_tag",
        lookup_expr="iexact")
    tf_gene = django_filters.CharFilter(
        field_name="tf__tf__gene",
        lookup_expr="iexact")

    class Meta:
        model = CCExperiment
        fields = ['id', 'experiment', 'experiment_id', 'batch',
                  'batch_replicate', 'tf_id', 'tf_locus_tag', 'tf_gene']
