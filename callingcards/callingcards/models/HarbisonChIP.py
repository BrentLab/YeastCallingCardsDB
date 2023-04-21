"""
.. module:: harbison_chip
   :synopsis: Module for the `HarbisonChIP` model that stores ChIP-seq
              experiments for the Harbison lab.

This module defines the `HarbisonChIP` model used to store ChIP-seq experiments
for the Harbison lab, including the `gene`, `tf`, and `pval` fields.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-21
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator  # pylint: disable=import-error # noqa # type: ignore
from .BaseModel import BaseModel
from .constants import P_VAL_DECIMAL_PLACES, P_VAL_MAX_DIGITS


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


class HarbisonChIP(BaseModel):
    """
    A model for storing ChIP-seq experiments for the Harbison lab.

    Fields:
        - `gene`: ForeignKey to the `Gene` model, representing the gene that 
          was targeted in the ChIP-seq experiment.
        - `tf`: ForeignKey to the `Gene` model, representing the transcription
          factor that was used in the ChIP-seq experiment.
        - `pval`: DecimalField with a max digits of 6 and decimal places of 4,
          representing the p-value of the ChIP-seq experiment.

    Example usage:

    .. code-block:: python

        from callingcards.models import HarbisonChIP

        # get all HarbisonChIP records
        all_harbisonchip = HarbisonChIP.objects.all()

    """
    objects = HarbisonChIPQuerySet.as_manager()

    # note that foreignkey fields automatically
    # create an index on the field
    gene = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='harbisonchip_target',
        db_index=True)
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='harbisonchip_tf',
        db_index=True)
    pval = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=P_VAL_MAX_DIGITS,
        decimal_places=P_VAL_DECIMAL_PLACES
    )

    class Meta:
        managed = True
        db_table = 'harbison_chip'