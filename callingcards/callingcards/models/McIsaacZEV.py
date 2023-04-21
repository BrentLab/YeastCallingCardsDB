"""
.. module:: mcisaac_zev
   :synopsis: Model for storing McIsaac ZEV data.

This module defines the `McIsaacZEV` model, which is used to store McIsaac ZEV
data along with the target gene and transcription factor.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .BaseModel import BaseModel
from .constants import (P_VAL_DECIMAL_PLACES, P_VAL_MAX_DIGITS,
                      EFFECT_DECIMAL_PLACES, EFFECT_MAX_DIGITS)


class McIsaacZEV(BaseModel):
    """
    A model for storing McIsaac ZEV data along with the target gene and
    transcription factor.

    Fields:
        - gene: ForeignKey to the `Gene` model, representing the target gene.
        - effect: DecimalField with the effect size of the transcription factor
          knockout on the target gene.
        - pval: DecimalField with the p-value of the Z-test for the
          transcription factor knockout on the target gene.
        - tf: ForeignKey to the `Gene` model, representing the transcription
          factor that was knocked out.

    Example usage:

    .. code-block:: python

        from callingcards.models import McIsaacZEV

        # get all McIsaacZEV records
        all_records = McIsaacZEV.objects.all()
    """
    gene = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='mcisaaczev_target')
    effect = models.DecimalField(
        max_digits=EFFECT_MAX_DIGITS,
        decimal_places=EFFECT_DECIMAL_PLACES
    )
    pval = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.0,
        null=False,
        max_digits=P_VAL_MAX_DIGITS,
        decimal_places=P_VAL_DECIMAL_PLACES)
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='mcisaaczev_tf',
        db_index=True)

    class Meta:
        managed = True
        db_table = 'mcisaac_zev'
