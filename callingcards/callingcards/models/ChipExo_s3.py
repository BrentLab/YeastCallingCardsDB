"""
.. module:: ChipExo_s3
   :synopsis: Model for storing ChipExo ZEV data.

This module defines the `ChipExo_s3` model, which is used to store ChipExo ZEV
data along with the target gene and transcription factor. Data is stored as 
a file by tf, strain, date, restriction, mechanism, and time. The file is
stored in S3 and the path to the file is stored in the database.
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.dispatch import receiver
from .BaseModel import BaseModel
from .filepaths.chipexo_filepath import chipexo_filepath

logger = logging.getLogger(__name__)


class ChipExo_s3(BaseModel):
    """
    A model for storing ChipExo ZEV data along with the target gene and
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

        from callingcards.models import ChipExo_s3

        # get all ChipExo_s3 records
        all_records = ChipExo_s3.objects.all()
    """

    CONDITION_CHOICES = [('YPD', 'YPD')]

    # the TF which was overexpressed. This foreign keys to
    # the gene table
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='chipexo_s3_tf',
        db_index=True)
    chipexo_id = models.CharField(
        max_length=15,
        null=False,
        blank=False)
    condition = models.DateField(
        null=False,
        blank=False,
        choices=CONDITION_CHOICES)
    parent_condition = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        choices=CONDITION_CHOICES)
    file = models.FileField(upload_to=chipexo_filepath)

    class Meta:
        managed = True
        db_table = 'chipexo_s3'


@receiver(models.signals.post_delete, sender=ChipExo_s3)
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
