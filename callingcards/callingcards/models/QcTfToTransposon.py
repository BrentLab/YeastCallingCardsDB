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


class QcTfToTransposon(BaseModel):
    """
    A model for storing information related to quality control metrics for
    Calling Cards experiments.

    Fields:
        - experiment: ForeignKey to the `CCExperiment` model, representing the
          calling card experiment associated with the quality control metrics.
        - edit_dist: IntegerField representing the edit distance for the
          experiment.
        - tally: IntegerField representing the tally count for the experiment.
        - note: CharField with a max length of 100, representing any additional
          comments related to the quality control metrics.

    Example usage:

    .. code-block:: python

        from callingcards.models import QcTfToTransposon

        # get all QcTfToTransposon records
        all_qc_metrics = QcTfToTransposon.objects.all()

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
        db_table = 'qc_tf_to_transposon'