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


class QcMetrics(BaseModel):
    """
    A model for storing information related to the manual quality control review
    of calling card experiments.

    Fields:
        - experiment: ForeignKey to the `CCExperiment` model, representing the
        calling card experiment associated with the quality control review.
        - rank_recall: CharField with a max length of 10, representing the
        ranking recall of the experiment.
        - chip_better: CharField with a max length of 10, representing whether
        the calling card performed better than the control.
        - data_usable: CharField with a max length of 10, representing whether
        the data was usable.
        - passing_replicate: CharField with a max length of 10, representing
        whether the replicate passed quality control.
        - note: CharField with a max length of 100, representing any additional
        comments related to the quality control review.

    Example usage:

    .. code-block:: python

        from callingcards.models import QcManualReview

        # get all QcManualReview records
        all_qc_reviews = QcManualReview.objects.all()

    """
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE,
        db_index=True)
    total_reads = models.PositiveIntegerField()
    unmapped = models.PositiveIntegerField()
    multimapped = models.PositiveIntegerField()
    genome_mapped = models.PositiveIntegerField()
    plasmid_mapped = models.IntegerField(
        validators=[MinValueValidator(-1)]
    )
    hpaii = models.PositiveIntegerField()
    hinp1i = models.PositiveIntegerField()
    taqai = models.PositiveIntegerField()
    undet = models.PositiveIntegerField()
    note = models.CharField(
        max_length=50,
        default='none'
    )

    class Meta:
        managed = True
        db_table = 'qc_alignment'
