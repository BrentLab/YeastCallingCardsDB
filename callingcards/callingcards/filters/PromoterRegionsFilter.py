import django_filters
from ..models import PromoterRegions


class PromoterRegionsFilter(django_filters.FilterSet):
    """
    PromoterRegionsFilter is a FilterSet for the PromoterRegions model.
    It allows filtering based on the following fields:

    - chr_ucsc: ucsc Chromosome ids (Foreign key to ChrMap model)
    - start: Start position
    - end: End position
    - strand: Strand (either '+', '-' or '.')
    - target_locus_tag: Associated feature locus_tag (Foreign key to Gene model)
    - target_gene: Associated feature gene name (Foreign key to Gene model)
    - score: Score (0-100)
    - source: Source (either 'not_orf' or 'yiming')
    """
    chr_ucsc = django_filters.CharFilter('chr__ucsc')
    target_locus_tag = django_filters.CharFilter(
        'associated_feature__locus_tag')
    target_gene = django_filters.CharFilter('associated_feature__gene')
    promoter_source = django_filters.CharFilter(field_name="source")

    class Meta:
        model = PromoterRegions
        fields = [
            'chr_ucsc',
            'start',
            'end',
            'strand',
            'target_locus_tag',
            'target_gene',
            'score',
            'source',
            'promoter_source',
        ]
