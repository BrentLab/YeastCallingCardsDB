"""Querysets for the callingcards app -- import these into models.py"""
from django.db import models


class PromoterRegionsQuerySet(models.QuerySet):
    def targets(self):
        return self\
            .select_related(
                'associated_feature',
            )\
            .annotate(
                promoter_id=models.F('id'),
                target_gene_id=models.F('associated_feature_id'),
                target_locus_tag=models.F('associated_feature__locus_tag'),
                target_gene=models.F('associated_feature__gene'))\
            .values('promoter_id', 'target_gene_id', 'target_locus_tag',
                    'target_gene', 'source')


class HopsReplicateSigQuerySet(models.QuerySet):
    def with_annotations(self):
        return self\
            .select_related(
                'cc_experiment',
                'promoter__associated_feature',
                'experiment__tf__tf',
            )\
            .annotate(
                tf_id_alias=models.F('experiment__tf__tf'),
                tf_locus_tag=models.F('experiment__tf__tf__locus_tag'),
                tf_gene=models.F('experiment__tf__tf__gene'),
                target_gene_id=models.F('promoter__associated_feature_id'),
                target_locus_tag=models.F(
                    'promoter__associated_feature__locus_tag'),
                target_gene=models.F('promoter__associated_feature__gene'),
                experiment_batch=models.F('experiment__batch'),
                experiment_batch_replicate=models.F(
                    'experiment__batch_replicate'),
                promoter_source=models.F('promoter__source'))\
            .values('tf_id_alias', 'tf_locus_tag', 'tf_gene',
                    'target_locus_tag', 'target_gene_id',
                    'target_gene', 'bg_hops', 'expr_hops',
                    'poisson_pval', 'hypergeom_pval', 'experiment',
                    'experiment_batch', 'experiment_batch_replicate',
                    'background', 'promoter_id', 'promoter_source')
    

class HarbisonChIPQuerySet(models.QuerySet):
    def with_annotations(self):
        return self\
            .select_related(
                'tf',
                'gene',
            )\
            .annotate(
                tf_locus_tag=models.F('tf__locus_tag'),
                tf_gene=models.F('tf__gene'),
                target_locus_tag=models.F('gene__locus_tag'),
                target_gene=models.F('gene__gene'),
                target_gene_id=models.F('gene_id'),
                binding_signal=models.F('pval'),
                experiment=models.Value('harbison'))\
            .values('tf_id', 'tf_locus_tag', 'tf_gene',
                    'target_gene_id', 'target_locus_tag', 'target_gene', 
                    'binding_signal', 'experiment')
    
class CCTFQuerySet(models.QuerySet):
    def tf_list(self):
        return self\
            .select_related(
                'tf',
            )\
            .annotate(   
                tf_locus_tag=models.F('tf__locus_tag'),
                tf_gene=models.F('tf__gene'),
            )\
            .values('tf_id', 'tf_locus_tag', 'tf_gene')

# from django.db.models import F, QuerySet, Prefetch
# from .models import (CCExperiment, HopsReplicateSig, McIsaacZEV,
#                      KemmerenTFKO, HarbisonChIP)

# class ChrMapQuerySet(QuerySet):
#     pass

# class GeneQuerySet(QuerySet):
#     def effects(self, promoter_source, cc_background, tf_gene):
#         cc_experiments = CCExperiment.objects.filter(tf__tf__gene=tf_gene)

#         return self\
#             .prefetch_related(
#                 Prefetch('genepromoter__hopsreplicatesig_set',
#                          queryset=HopsReplicateSig.objects
#                          .filter(background=cc_background,
#                                  promoter__source=promoter_source,
#                                  experiment__in=cc_experiments)),
#                 Prefetch('harbisonchip_target',
#                          queryset=HarbisonChIP.objects
#                          .filter(tf__gene=tf_gene)),
#                 Prefetch('mcisaaczev_target',
#                          queryset=McIsaacZEV.objects
#                          .filter(tf__gene=tf_gene)),
#                 Prefetch('kemmerentfko_target',
#                          queryset=KemmerenTFKO.objects
#                          .filter(tf__gene=tf_gene))
#             )\
#             .annotate(
#                 tf_id=F('genepromoter__hopsreplicatesig__experiment__tf__tf_id'),
#                 tf_locus_tag=F('genepromoter__hopsreplicatesig__experiment__tf__tf__locus_tag'),
#                 tf_gene=F('genepromoter__hopsreplicatesig__experiment__tf__tf__gene'),
#                 target_gene_id=F('id'),
#                 target_locus_tag=F('locus_tag'),
#                 target_gene=F('gene'),
#                 binding_cc_experiment=F('genepromoter__hopsreplicatesig__experiment'),
#                 binding_cc_batch=F('genepromoter__hopsreplicatesig__experiment__batch'),
#                 binding_cc_batch_replicate=F('genepromoter__hopsreplicatesig__experiment__batch_replicate'),
#                 binding_cc_pval=F('genepromoter__hopsreplicatesig__poisson_pval'),
#                 binding_harbison_pval=F('harbisonchip_target__pval'),
#                 expression_effect_mcisaaczev=F('mcisaaczev_target__effect'),
#                 expression_pval_mcisaaczev=F('mcisaaczev_target__pval'),
#                 expression_effect_kemmerentfko=F('kemmerentfko_target__effect'),
#                 expression_pval_kemmerentfko=F('kemmerentfko_target__padj'))\
#             .values('tf_id', 'tf_locus_tag', 'tf_gene', 'target_gene_id',
#                     'target_locus_tag', 'target_gene', 'binding_cc_experiment',
#                     'binding_cc_batch', 'binding_cc_batch_replicate',
#                     'binding_cc_pval', 'binding_harbison_pval',
#                     'expression_effect_mcisaaczev',
#                     'expression_pval_mcisaaczev',
#                     'expression_effect_kemmerentfko',
#                     'expression_pval_kemmerentfko')


# class PromoterRegionsQuerySet(QuerySet):
#     def targets(self):
#         return self\
#             .select_related(
#                 'associated_feature',
#             )\
#             .annotate(
#                 promoter_id=F('id'),
#                 target_gene_id=F('associated_feature_id'),
#                 target_locus_tag=F('associated_feature__locus_tag'),
#                 target_gene=F('associated_feature__gene'))\
#             .values('promoter_id', 'target_gene_id', 'target_locus_tag',
#                     'target_gene', 'source')

# class HarbisonChIPQuerySet(QuerySet):
#     def with_annotations(self):
#         return self\
#             .select_related(
#                 'tf',
#                 'gene',
#             )\
#             .annotate(
#                 tf_locus_tag=F('tf__locus_tag'),
#                 tf_gene=F('tf__gene'),
#                 target_locus_tag=F('gene__locus_tag'),
#                 target_gene=F('gene__gene'),
#                 target_gene_id=F('gene_id'))\
#             .values('tf_locus_tag', 'tf_gene', 'target_locus_tag',
#                     'target_gene', 'pval', 'target_gene_id', 'tf_id')


# class KemmerenTFKOQuerySet(QuerySet):
#     pass

# class McIsaacZEVQuerySet(QuerySet):
#     pass

# class BackgroundQuerySet(QuerySet):
#     pass

# class CCTFQuerySet(QuerySet):
#     pass

# class CCExperimentQuerySet(QuerySet):
#     pass

# class HopsQuerySet(QuerySet):
#     pass

# class HopsReplicateSigQuerySet(QuerySet):
#     def with_annotations(self):
#         return self\
#             .select_related(
#                 'cc_experiment',
#                 'promoter__associated_feature',
#                 'experiment__tf__tf',
#             )\
#             .annotate(
#                 tf_id_alias=F('experiment__tf__tf'),
#                 tf_locus_tag=F('experiment__tf__tf__locus_tag'),
#                 tf_gene=F('experiment__tf__tf__gene'),
#                 target_gene_id=F('promoter__associated_feature_id'),
#                 target_locus_tag=F('promoter__associated_feature__locus_tag'),
#                 target_gene=F('promoter__associated_feature__gene'),
#                 experiment_batch=F('experiment__batch'),
#                 experiment_batch_replicate=F('experiment__batch_replicate'),
#                 promoter_source=F('promoter__source'))\
#             .values('tf_id_alias', 'tf_locus_tag', 'tf_gene',
#                     'target_locus_tag', 'target_gene_id',
#                     'target_gene', 'bg_hops', 'expr_hops',
#                     'poisson_pval', 'hypergeom_pval', 'experiment',
#                     'experiment_batch', 'experiment_batch_replicate',
#                     'background', 'promoter_id', 'promoter_source')

# class QcMetricsQuerySet(QuerySet):
#     pass

# class QcManualReviewQuerySet(QuerySet):
#     pass

# class QcR1ToR2TfQuerySet(QuerySet):
#     pass

# class QcR2ToR1TfQuerySet(QuerySet):
#     pass


# class QcTfToTransposonQuerySet(QuerySet):
#     pass
