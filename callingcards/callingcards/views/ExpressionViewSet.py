from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Value
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .mixins import (ListModelFieldsMixin, CustomCreateMixin,
                     PageSizeModelMixin, CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..serializers import ExpressionViewSetSerializer
from ..filters import McIsaacZevFilter, KemmerenTfkoFilter

class ExpressionViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        CustomValidateMixin,
                        UpdateModifiedMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    ExpressionViewSet returns gene expression data for genes
    that have both McIsaac ZEV and Kemmeren TF-KO effect values.
    """
    serializer_class = ExpressionViewSetSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['source_expr', 'tf_expr', 'rank_expr']
    custom_filter_columns = ['tf_id', 'gene_id', 'effect',
                             'tf_locus_tag', 'tf_gene', 'target_locus_tag',
                             'target_gene']

    def get_queryset(self):

        return_fields = ['tf_id_alias', 'tf_locus_tag', 'tf_gene',
                         'target_gene_id', 'target_locus_tag', 'target_gene',
                         'effect_expr', 'p_expr', 'source_expr']

        # Get query parameters for filtering
        mcisaac_filter = McIsaacZevFilter(self.request.GET)
        kemmeren_filter = KemmerenTfkoFilter(self.request.GET)

        mcisaac_filtered_qs = mcisaac_filter.qs\
            .annotate(
                tf_id_alias=F('tf_id'),
                tf_locus_tag=F('tf_id__locus_tag'),
                tf_gene=F('tf_id__gene'),
                target_gene_id=F('gene_id'),
                target_locus_tag=F('gene_id__locus_tag'),
                target_gene=F('gene_id__gene'),
                effect_expr=F('effect'),
                p_expr=F('pval'),
                source_expr=Value('mcisaac_zev'))\
            .values(*return_fields)

        kemmeren_filtered_qs = kemmeren_filter.qs\
            .annotate(
                tf_id_alias=F('tf_id'),
                tf_locus_tag=F('tf_id__locus_tag'),
                tf_gene=F('tf_id__gene'),
                target_gene_id=F('gene_id'),
                target_locus_tag=F('gene_id__locus_tag'),
                target_gene=F('gene_id__gene'),
                effect_expr=F('effect'),
                p_expr=F('padj'),
                source_expr=Value('kemmeren_tfko'))\
            .values(*return_fields)

        # Combine the two querysets and order by 'tf' and 'gene'
        concatenated_query = mcisaac_filtered_qs\
            .union(kemmeren_filtered_qs)\
            .order_by('source_expr', 'tf_id_alias')

        return concatenated_query

    @action(detail=False, methods=['get'])
    def fields(self, request, *args, **kwargs):

        # Get the _readable_fields attribute of the dummy serializer instance
        readable = ['tf_alias', 'gene_alias', 'effect_expr',
                    'p_expr', 'source_expr']
        writable = None
        automatically_generated = None

        try:
            filter_columns = self.filterset_class.Meta.fields
        except AttributeError:
            # Use the custom_filter_columns attribute if available
            # this needs to be set in the viewset class when there is no
            # filterset_class
            filter_columns = getattr(self, 'custom_filter_columns', None)

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writable": writable,
                         "automatically_generated":
                         automatically_generated,
                         "filter": filter_columns},
                        status=status.HTTP_200_OK)
