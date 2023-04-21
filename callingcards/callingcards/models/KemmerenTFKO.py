
"""
.. module:: kemmeren_tfko
   :synopsis: Model for storing the effects of transcription factor knockouts on
              gene expression.

This module provides the `KemmerenTFKO` model, which is used to store the
effects of transcription factor knockouts on gene expression.

.. author:: Chase Mateusiak
.. date:: 2023-04-20
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .BaseModel import BaseModel
from .constants import (P_VAL_DECIMAL_PLACES, P_VAL_MAX_DIGITS,
                      EFFECT_DECIMAL_PLACES, EFFECT_MAX_DIGITS)


class KemmerenTFKO(BaseModel):
    """
    A model for storing the effects of transcription factor knockouts on gene
    expression.

    Fields:
        - gene: ForeignKey to the `Gene` model, representing the gene whose
          expression was affected by a transcription factor knockout.
        - effect: DecimalField with a maximum number of digits and decimal
          places, representing the effect of the knockout on the expression of
          the target gene.
        - padj: DecimalField with a maximum number of digits and decimal places,
          representing the adjusted p-value for the effect of the knockout on
          the expression of the target gene.
        - tf: ForeignKey to the `Gene` model, representing the transcription
          factor whose knockout caused the effect on the target gene's
          expression.

    Example usage:

    .. code-block:: python

        from callingcards.models import KemmerenTFKO

        # get all KemmerenTFKO records
        all_records = KemmerenTFKO.objects.all()
    """
    gene = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='kemmerentfko_target')
    effect = models.DecimalField(
        max_digits=EFFECT_MAX_DIGITS,
        decimal_places=EFFECT_DECIMAL_PLACES
    )
    padj = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=P_VAL_MAX_DIGITS,
        decimal_places=P_VAL_DECIMAL_PLACES)
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='kemmerentfko_tf',
        db_index=True)

    class Meta:
        managed = True
        db_table = 'kemmeren_tfko'
