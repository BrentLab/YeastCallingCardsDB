"""
Module for storing quality control metrics.

This module provides a model for storing quality control metrics for Calling Cards experiments. 
Metrics include the total number of reads, the number of reads that were unmapped or mapped to 
multiple locations, the number of reads that mapped to the genome or plasmid, and the number of 
reads that were detected with specific restriction enzymes.

.. author:: Chase Mateusiak
.. date:: 2023-04-20
"""
from django.db import models
from django.core.validators import MinValueValidator
from .BaseModel import BaseModel


class QcR2ToR1Tf(BaseModel):
    """
    A model for storing information about the quality control of the reverse
    complement reads.

    Fields:
        - experiment: ForeignKey to the `CCExperiment` model, representing the
          calling card experiment associated with the quality control review.
        - edit_dist: IntegerField representing the edit distance between the
          forward and reverse complement reads.
        - tally: IntegerField representing the number of times the read was
          observed.
        - note: CharField with a max length of 100, representing any additional
          comments related to the quality control review.

    Example usage:

    .. code-block:: python

        from callingcards.models import QcR2ToR1Tf

        # get all QcR2ToR1Tf records
        all_qc_records = QcR2ToR1Tf.objects.all()

    """
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE,
        db_index=True)
    edit_dist = models.IntegerField()
    tally = models.IntegerField(
        validators=[MinValueValidator(-1)]
    )
    note = models.CharField(
        max_length=100,
        default='none'
    )

    class Meta:
        managed = True
        db_table = 'qc_r2_to_r1_tf'
