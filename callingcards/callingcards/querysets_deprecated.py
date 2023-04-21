"""Querysets for the callingcards app -- import these into models.py"""
# from django.db import models


# class PromoterRegionsQuerySet(models.QuerySet):
#     def targets(self):
#         return self\
#             .select_related(
#                 'associated_feature',
#             )\
#             .annotate(
#                 promoter_id=models.F('id'),
#                 target_gene_id=models.F('associated_feature_id'),
#                 target_locus_tag=models.F('associated_feature__locus_tag'),
#                 target_gene=models.F('associated_feature__gene'))\
#             .values('promoter_id', 'target_gene_id', 'target_locus_tag',
#                     'target_gene', 'source')


# class HopsReplicateSigQuerySet(models.QuerySet):
#     def with_annotations(self):
#         return self\
#             .select_related(
#                 'cc_experiment',
#                 'promoter__associated_feature',
#                 'experiment__tf__tf',
#             )\
#             .annotate(
#                 tf_id_alias=models.F('experiment__tf__tf'),
#                 tf_locus_tag=models.F('experiment__tf__tf__locus_tag'),
#                 tf_gene=models.F('experiment__tf__tf__gene'),
#                 target_gene_id=models.F('promoter__associated_feature_id'),
#                 target_locus_tag=models.F(
#                     'promoter__associated_feature__locus_tag'),
#                 target_gene=models.F('promoter__associated_feature__gene'),
#                 experiment_batch=models.F('experiment__batch'),
#                 experiment_batch_replicate=models.F(
#                     'experiment__batch_replicate'),
#                 promoter_source=models.F('promoter__source'))\
#             .values('tf_id_alias', 'tf_locus_tag', 'tf_gene',
#                     'target_locus_tag', 'target_gene_id',
#                     'target_gene', 'bg_hops', 'expr_hops',
#                     'poisson_pval', 'hypergeom_pval', 'experiment',
#                     'experiment_batch', 'experiment_batch_replicate',
#                     'background', 'promoter_id', 'promoter_source')
    

# class HarbisonChIPQuerySet(models.QuerySet):
#     def with_annotations(self):
#         return self\
#             .select_related(
#                 'tf',
#                 'gene',
#             )\
#             .annotate(
#                 tf_locus_tag=models.F('tf__locus_tag'),
#                 tf_gene=models.F('tf__gene'),
#                 target_locus_tag=models.F('gene__locus_tag'),
#                 target_gene=models.F('gene__gene'),
#                 target_gene_id=models.F('gene_id'),
#                 binding_signal=models.F('pval'),
#                 experiment=models.Value('harbison'))\
#             .values('tf_id', 'tf_locus_tag', 'tf_gene',
#                     'target_gene_id', 'target_locus_tag', 'target_gene', 
#                     'binding_signal', 'experiment')
    
# class CCTFQuerySet(models.QuerySet):
#     def tf_list(self):
#         return self\
#             .select_related(
#                 'tf',
#             )\
#             .annotate(   
#                 tf_locus_tag=models.F('tf__locus_tag'),
#                 tf_gene=models.F('tf__gene'),
#             )\
#             .values('tf_id', 'tf_locus_tag', 'tf_gene')
