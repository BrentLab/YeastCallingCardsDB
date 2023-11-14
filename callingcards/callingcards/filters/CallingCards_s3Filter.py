import django_filters
from ..models import CallingCards_s3


class CallingCards_s3Filter(django_filters.FilterSet):
    tf_id = django_filters.NumberFilter(field_name="experiment__tf__tf__id")
    tf_locus_tag = django_filters.CharFilter(
        field_name="experiment__tf__tf__locus_tag")
    tf_gene = django_filters.CharFilter(field_name="experiment__tf__tf__gene")
    experiment_id = django_filters.CharFilter(field_name="experiment__id")
    batch = django_filters.CharFilter(field_name="experiment__batch")
    hops_source = django_filters.CharFilter(field_name="source__source")

    class Meta:
        model = CallingCards_s3
        fields = ['tf_id', 'tf_locus_tag', 'tf_gene', 
                  'experiment_id', 'batch', 'hops_source']
