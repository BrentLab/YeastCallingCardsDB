"""
.. module:: qc_manual_review
   :synopsis: Model for manual quality control review of calling card experiments.

This module defines the `QcManualReview` model, which stores information related
to the manual quality control review of calling card experiments.

This model includes fields for ranking recall, whether the chip performed better
than the control, whether the data was usable, and whether the replicate passed
the quality control. It also includes a note field for any additional comments.

This model is related to the `CCExperiment` model.

.. seealso:: :class:`callingcards.models.CCExperiment`

"""
from django.db import models
from .BaseModel import BaseModel


class QcManualReview(BaseModel):
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

    PASS = 'pass'
    FAIL = 'fail'

    YES = 'yes'
    NO = 'no'
    NOTE = 'note'

    UNREVIEWED = 'unreviewed'

    PASS_FAIL = ((PASS, 'pass'),
                 (FAIL, 'fail'),
                 (UNREVIEWED, 'unreviewed'),
                 (NOTE, 'note'))

    YES_NO = ((YES, 'yes'),
              (NO, 'no'),
              (UNREVIEWED, 'unreviewed'),
              (NOTE, 'note'))

    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE,
        db_index=True)
    rank_recall = models.CharField(
        max_length=10,
        choices=PASS_FAIL,
        default=UNREVIEWED)
    chip_better = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=UNREVIEWED)
    data_usable = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=UNREVIEWED)
    passing_replicate = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=UNREVIEWED)
    note = models.CharField(
        max_length=100,
        default='none'
    )

    class Meta:
        managed = True
        db_table = 'qc_manual_review'