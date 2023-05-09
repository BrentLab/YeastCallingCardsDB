import django_filters
from ..models import McIsaacZEV


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
