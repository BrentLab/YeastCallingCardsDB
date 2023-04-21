"""
.. module:: hops_replicate_sig
   :synopsis: Module for the `HopsReplicateSig` model that stores HOPS
              replicate significance data.

This module defines the `HopsReplicateSig` model used to store HOPS replicate
significance data, including the `experiment`, `promoter`, `bg_hops`,
`expr_hops`, `effect`, `poisson_pval`, `hypergeom_pval`, and `background`
fields.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-21
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator  # pylint: disable=import-error # noqa # type: ignore
from .BaseModel import BaseModel
from .constants import (P_VAL_DECIMAL_PLACES, P_VAL_MAX_DIGITS,
                      EFFECT_DECIMAL_PLACES, EFFECT_MAX_DIGITS)
from .Background import Background


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
    
    
class HopsReplicateSig(BaseModel):
    """
    A model for storing HOPS replicate significance data.

    Fields:
        - `experiment`: ForeignKey to the `CCExperiment` model, representing
          the experiment associated with the HOPS replicate significance data.
        - `promoter`: ForeignKey to the `PromoterRegions` model, representing
          the promoter region associated with the HOPS replicate significance
          data.
        - `bg_hops`: PositiveIntegerField representing the number of HOPS reads
          in the background.
        - `expr_hops`: PositiveIntegerField representing the number of HOPS
          reads in the experiment.
        - `effect`: DecimalField with a max length of 8 and decimal places of 6,
          representing the effect size.
        - `poisson_pval`: DecimalField with a max length of 8 and decimal places
          of 6, representing the Poisson p-value.
        - `hypergeom_pval`: DecimalField with a max length of 8 and decimal
          places of 6, representing the hypergeometric p-value.
        - `background`: CharField with a max length of 10 and choices of `'input'`
          or `'background'`, representing whether the data comes from input or
          background samples.

    Example usage:

    .. code-block:: python

        from callingcards.models import HopsReplicateSig

        # get all HopsReplicateSig records
        all_hops_replicate_sig = HopsReplicateSig.objects.all()

    """

    objects = HopsReplicateSigQuerySet.as_manager()

    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE,
        db_index=True)
    promoter = models.ForeignKey(
        'PromoterRegions',
        models.PROTECT,
        db_index=True)
    bg_hops = models.PositiveIntegerField()
    expr_hops = models.PositiveIntegerField()
    poisson_pval = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=P_VAL_MAX_DIGITS,
        decimal_places=P_VAL_DECIMAL_PLACES
    )
    hypergeom_pval = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=P_VAL_MAX_DIGITS,
        decimal_places=P_VAL_DECIMAL_PLACES
    )
    background = models.CharField(
        max_length=10,
        choices=Background.SOURCE_CHOICES
    )

    class Meta:
        managed = True
        db_table = 'hops_replicate_sig'
