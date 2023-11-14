"""
.. module:: ChipExoSig
   :synopsis: Model for storing the score associated with a given set of
    promoter regions.

This module defines the table which stores the bed files which define the
    score of a given promoter set for a given ChipExo experiment.
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.dispatch import receiver
from .BaseModel import BaseModel
from .filepaths.chipexosigregions_filepath import chipexosigregions_filepath

logger = logging.getLogger(__name__)


class ChipExoSig(BaseModel):
    """
    This table stores files which assign a ChipExo score to a given set of
    genomic regions

    Fields:
        - chipexodata_id: Foreign key to the ChipExo_s3 table
        - promoterregions_id: Foreign key to the PromoterRegions table
        - file: the path to the bed file containing the ChipExo score for the
            promoter regions

    Example usage:

    .. code-block:: python

        from callingcards.models import ChipExoSig

        # get all ChipExoSig records
        all_records = ChipExoSig.objects.all()
    """
    chipexodata_id = models.ForeignKey(
        'ChipExo_s3',
        models.CASCADE,
        related_name='chipexodata_id',
        db_index=True,
        help_text="The ChipExo_s3 id for which the ChipExo score is defined")
    promoterregions_id = models.ForeignKey(
        'PromoterRegions_s3',
        models.CASCADE,
        related_name='promoterregions_id',
        db_index=True,
        help_text="The promoterregions_id for which the ChipExo score is "
        "defined")
    file = models.FileField(upload_to=chipexosigregions_filepath,
                            help_text="The path to a bed file containing the "
                                      "ChipExo score for a set of regions")

    class Meta:
        managed = True
        db_table = 'ChipExoSig'


@receiver(models.signals.post_delete, sender=ChipExoSig)
def remove_file_from_s3(sender, instance, using, **kwargs):
    """
    this is a post_delete signal. Hence, if the delete command is successful,
    the file will be deleted. If the delete command is successful, and for some
    reason the delete signal fails, it is possible to end up with files in S3
    which are not referenced by the database.
    upon inception, there did not exist any images which were not referenced.
    So,if unreferenced files are ever found, that should indicate that these
    files are erroneous and can be safely deleted
    """
    # note that if the directory (and all subdirectories) are empty, the
    # directory will also be removed
    instance.file.delete(save=False)
