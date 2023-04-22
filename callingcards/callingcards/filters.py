import django_filters
from .models.mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin
from .models import (Gene, McIsaacZEV, KemmerenTFKO, Background,
                     Hops, HopsReplicateSig, CCExperiment,
                     PromoterRegions, HarbisonChIP, QcMetrics,
                     QcManualReview, QcR1ToR2Tf, QcR2ToR1Tf,
                     QcTfToTransposon)

class HopsFilter(django_filters.FilterSet):
    tf_id = django_filters.NumberFilter(field_name="experiment__tf__id")
    tf_locus_tag = django_filters.CharFilter(field_name="experiment__tf__locus_tag")
    tf_gene = django_filters.CharFilter(field_name="experiment__tf__gene")
    experiment = django_filters.CharFilter(field_name="experiment__id")

    class Meta:
        model = Hops
        fields = ['tf_id', 'tf_locus_tag', 'tf_gene', 'experiment']


class BackgroundFilter(django_filters.FilterSet):
    background_source = django_filters.CharFilter(field_name="source")

    class Meta:
        model = Background
        fields = [f.name for f in model._meta.fields if f.name != 'source']
        fields += ['background_source']

class GeneFilter(django_filters.FilterSet):
    chr = django_filters.CharFilter(field_name="chr__ucsc")
    start = django_filters.NumberFilter()
    end = django_filters.NumberFilter()
    strand = django_filters.ChoiceFilter(
        choices=GenonomicCoordinatesMixin.STRAND_CHOICES)
    type = django_filters.CharFilter(lookup_expr='iexact')
    gene_biotype = django_filters.CharFilter(lookup_expr='iexact')
    locus_tag = django_filters.CharFilter(lookup_expr='iexact')
    gene = django_filters.CharFilter(lookup_expr='iexact')
    source = django_filters.CharFilter(lookup_expr='iexact')
    alias = django_filters.CharFilter(lookup_expr='iexact')
    note = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Gene
        fields = [
            'chr', 'start', 'end', 'strand', 'type', 'gene_biotype',
            'locus_tag', 'gene', 'source', 'alias', 'note'
        ]

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
    target_locus_tag = django_filters.CharFilter('associated_feature__locus_tag')
    target_gene = django_filters.CharFilter('associated_feature__gene')

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
        ]


class McIsaacZevFilter(django_filters.FilterSet):
    """
    McIsaacZevFilter is a FilterSet for the McIsaacZEV model. 
      It allows filtering based on the following fields:

    - tf_id: Transcription factor ID (Foreign key to Gene model)
    - gene_id: Gene ID (Foreign key to Gene model)
    - effect: Effect value of the gene expression
    - tf_locus_tag: Locus tag of the related transcription factor 
      (case-insensitive partial match)
    - tf_gene: Name of the related transcription factor 
      (case-insensitive partial match)
    - target_locus_tag: Locus tag of the related gene 
      (case-insensitive partial match)
    - target_gene: Name of the related gene (case-insensitive partial match)
    """
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
        model = McIsaacZEV
        fields = ['tf_id', 'gene_id', 'effect',
                  'tf_locus_tag', 'tf_gene', 'target_locus_tag', 'target_gene']


class KemmerenTfkoFilter(django_filters.FilterSet):
    """
    KemmerenTfkoFilter is a FilterSet for the KemmerenTFKO model. 
      It allows filtering based on the following fields:

    - tf_id: Transcription factor ID (Foreign key to Gene model)
    - gene_id: Gene ID (Foreign key to Gene model)
    - effect: Effect value of the gene expression
    - tf_locus_tag: Locus tag of the related transcription factor 
        (case-insensitive partial match)
    - tf_gene: Name of the related transcription factor 
        (case-insensitive partial match)
    - target_locus_tag: Locus tag of the related gene 
        (case-insensitive partial match)
    - target_gene: Name of the related gene (case-insensitive partial match)
    """
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
        model = KemmerenTFKO
        fields = ['tf_id', 'gene_id', 'effect',
                  'tf_locus_tag', 'tf_gene', 'target_locus_tag', 'target_gene']


class HarbisonChIPFilter(django_filters.FilterSet):
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
        model = HarbisonChIP
        fields = ['tf_id', 'tf_locus_tag', 'tf_gene',
                  'target_locus_tag', 'target_gene']

class CCExperimentFilter(django_filters.FilterSet):
    experiment = django_filters.NumberFilter(
        field_name="pk",
        lookup_expr="in")
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
        fields = ['experiment', 'batch', 'batch_replicate',
                  'tf_id', 'tf_locus_tag', 'tf_gene']


class HopsReplicateSigFilter(django_filters.FilterSet):

    batch = django_filters.CharFilter(
        field_name='experiment__batch',
        lookup_expr="iexact")
    batch_replicate = django_filters.NumberFilter(
        field_name='experiment__batch_replicate',
        lookup_expr="iexact")
    background = django_filters.CharFilter(
        field_name='background',
        lookup_expr="iexact")
    promoter_source = django_filters.CharFilter(
        field_name='promoter__source',
        lookup_expr="iexact")
    tf_id = django_filters.NumberFilter(
        field_name='experiment__tf__tf__id',
        lookup_expr="exact")
    tf_locus_tag = django_filters.CharFilter(
        field_name='experiment__tf__tf__locus_tag',
        lookup_expr="iexact")
    tf_gene = django_filters.CharFilter(
        field_name='experiment__tf__tf__gene',
        lookup_expr="iexact")
    target_locus_tag = django_filters.CharFilter(
        field_name='promoter__associated_feature__locus_tag',
        lookup_expr="iexact")
    target_gene = django_filters.CharFilter(
        field_name='promoter__associated_feature__gene',
        lookup_expr="iexact")

    class Meta:
        model = HopsReplicateSig
        fields = ['experiment', 'batch', 'batch_replicate', 'background',
                  'promoter_source', 'tf_id', 'tf_locus_tag', 'tf_gene',
                  'target_locus_tag', 'target_gene']


class QcMetricsFilter(django_filters.FilterSet):

    class Meta:
        model = QcMetrics
        fields = "__all__"


class QcManualReviewFilter(django_filters.FilterSet):

    class Meta:
        model = QcManualReview
        fields = "__all__"


class QcR1ToR2TfFilter(django_filters.FilterSet):

    class Meta:
        model = QcR1ToR2Tf
        fields = "__all__"


class QcR2ToR1TfFilter(django_filters.FilterSet):

    class Meta:
        model = QcR2ToR1Tf
        fields = "__all__"


class QcTfToTransposonFilter(django_filters.FilterSet):

    class Meta:
        model = QcTfToTransposon
        fields = "__all__"
