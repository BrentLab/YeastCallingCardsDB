"""
Module for storing quality control metrics related to the R1 to R2 transition.

This module provides a model for storing quality control metrics related to the R1 to R2 transition 
in Calling Cards experiments. Metrics include the edit distance, the tally, and any additional 
notes related to the quality control review.

Author: Chase Mateusiak
Date: 2023-04-20
"""
from django.db import models
from django.core.validators import MinValueValidator
from .BaseModel import BaseModel


class QcR1ToR2Tf(BaseModel):
    """
    A model for storing information about quality control of the Read 1 to Read 2
    transfer frequency for calling card experiments.

    Fields:
        - experiment: ForeignKey to the `CCExperiment` model, representing the
          calling card experiment associated with the quality control review.
        - edit_dist: PositiveSmallIntegerField, representing the edit distance
          between the Read 1 and Read 2 sequences.
        - tally: IntegerField, representing the number of pairs of reads that
          met the specified criteria.
        - note: CharField with a max length of 100, representing any additional
          comments related to the quality control review.

    Example usage:

    .. code-block:: python

        from callingcards.models import QcR1ToR2Tf

        # get all QcR1ToR2Tf records
        all_qc_r1_r2_tf = QcR1ToR2Tf.objects.all()

    """
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE,
        db_index=True)
    edit_dist = models.PositiveSmallIntegerField()
    tally = models.IntegerField(
        validators=[MinValueValidator(-1)]
    )
    note = models.CharField(
        max_length=100,
        default='none'
    )

    class Meta:
        managed = True
        db_table = 'qc_r1_to_r2_tf'