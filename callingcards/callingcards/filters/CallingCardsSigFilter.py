import django_filters
from ..models.mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin
from ..models import CallingCardsSig


class CallingCardsSigFilter(django_filters.FilterSet):
    tf_id = django_filters.NumberFilter('experiment__tf__tf__id')
    tf_locus_tag = django_filters.CharFilter('experiment__tf__tf__locus_tag')
    tf_gene = django_filters.CharFilter('experiment__tf__tf__gene')
    experiment_id = django_filters.NumberFilter('experiment__id')
    hops_source_id = django_filters.CharFilter('hops_source__id')
    background_source_id = django_filters.CharFilter('background__id')
    promoter_source_id = django_filters.CharFilter('promoter_source__id')

    class Meta:
        model = CallingCardsSig
        fields = ['experiment', 'experiment_id',
                  'tf_id', 'tf_locus_tag', 'tf_gene',
                  'hops_source', 'hops_source_id',
                  'background_source', 'background_source_id',
                  'promoter_source', 'promoter_source_id']
