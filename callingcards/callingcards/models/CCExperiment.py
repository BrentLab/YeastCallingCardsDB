"""
.. module:: CCExperiment
   :synopsis: Model for keeping a record of transcription factor batches.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-20

This module defines the `CCExperiment` model, which is used to keep a record of
the batches (most likely runs) in which a given set of transcription factors
were interrogated with calling cards.
"""
from django.db import models
from .BaseModel import BaseModel


class CCExperiment(BaseModel):
    """
    A model for keeping a record of the batches (most likely runs) in which a
    given set of transcription factors were interrogated with calling cards.

    Fields:
        - batch: CharField with a max length of 15, representing the batch or run
          number in which a given set of transcription factors were
          interrogated.
        - tf: ForeignKey to the CCTF model, representing the transcription
          factor(s) that were interrogated in a given batch.
        - batch_replicate: PositiveSmallIntegerField, representing a unique
          identifier for a given batch or run number.

    Example usage:

    .. code-block:: python

        from callingcards.models import CCExperiment

        # get all CCExperiment records
        all_experiments = CCExperiment.objects.all()

    """
    # likely a run number, eg run_1234
    batch = models.CharField(
        max_length=15
    )
    # id of a record in the gene table
    tf = models.ForeignKey(
        'CCTF',
        models.CASCADE,
        db_index=True)
    # when the same tf is used in multiple experiments, each sample should be
    # uniquely identified by batch_replicate
    batch_replicate = models.PositiveSmallIntegerField(
        default=1)
    lab = models.ForeignKey(
        'lab',
        models.CASCADE,
        db_index=True)

    def __str__(self):
        return (str(self.batch) + '; '
                + str(self.tf) + '; '
                + 'batch_rep: ' + str(self.batch_replicate) + '; '
                + 'ID: ' + str(self.id))  # pylint: disable=no-member

    class Meta:
        managed = True
        db_table = 'cc_experiment'
