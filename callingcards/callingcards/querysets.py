"""Querysets for the callingcards app -- import these into models.py"""

from django.db.models import F, QuerySet

class HarbisonChIPQuerySet(QuerySet):
    def with_annotations(self):
        return self\
            .select_related(
                'tf',
                'gene',
            )\
            .annotate(
                tf_locus_tag=F('tf__locus_tag'),
                tf_gene=F('tf__gene'),
                target_locus_tag=F('gene__locus_tag'),
                target_gene=F('gene__gene'))\
            .values('tf_locus_tag', 'tf_gene', 'target_locus_tag',
                    'target_gene', 'pval', 'gene_id', 'tf_id')


class HopsReplicateSigQuerySet(QuerySet):
    def with_annotations(self):
        return self\
            .select_related(
                'cc_experiment',
                'promoter__associated_feature',
                'experiment__tf__tf',
            )\
            .annotate(
                tf_locus_tag=F('experiment__tf__tf__locus_tag'),
                tf_gene=F('experiment__tf__tf__gene'),
                target_locus_tag=F('promoter__associated_feature__locus_tag'),
                target_gene=F('promoter__associated_feature__gene'),
                experiment_batch=F('experiment__batch'),
                experiment_batch_replicate=F('experiment__batch_replicate'),
                promoter_source=F('promoter__source'))\
            .values('tf_locus_tag', 'tf_gene', 'target_locus_tag',
                    'target_gene', 'bg_hops', 'expr_hops',
                    'poisson_pval', 'hypergeom_pval', 'experiment',
                     'experiment_batch', 'experiment_batch_replicate', 
                     'background', 'promoter_id', 'promoter_source')
