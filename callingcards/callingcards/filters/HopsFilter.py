import django_filters
from ..models import Hops


class HopsFilter(django_filters.FilterSet):
    tf_id = django_filters.NumberFilter(field_name="experiment__tf__tf__id")
    tf_locus_tag = django_filters.CharFilter(
        field_name="experiment__tf__tf__locus_tag")
    tf_gene = django_filters.CharFilter(field_name="experiment__tf__tf__gene")
    experiment = django_filters.CharFilter(field_name="experiment__id")
    experiment_id = django_filters.CharFilter(field_name="experiment__id")

    class Meta:
        model = Hops
        fields = ['tf_id', 'tf_locus_tag', 'tf_gene',
                  'experiment', 'experiment_id']
