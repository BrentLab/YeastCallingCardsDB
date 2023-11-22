"""
.. module:: ChipExo_s3
   :synopsis: Model for storing ChipExo ZEV data.

This module defines the `ChipExo_s3` model, which is used to store ChipExo ZEV
data along with the target gene and transcription factor. Data is stored as 
a file by regulator, strain, date, restriction, mechanism, and time. The file is
stored in S3 and the path to the file is stored in the database.
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator  # pylint: disable=import-error # noqa # type: ignore
from .BaseModel import BaseModel
from .mixins.FileUploadWithIdMixin import FileUploadMixin
from .filepaths.chipexo_filepath import chipexo_filepath

logger = logging.getLogger(__name__)


class ChipExo_s3(BaseModel, FileUploadMixin):
    """
    A model for storing ChipExo data from yeastepigenome.org

    Fields:
        - regulator: the TF assayed in the ChipExo data
        - chipexo_id: the unique identifier for the ChipExo data from
            yeastepigenome.org
        - condition: the condition under which the ChipExo data was collected
        - parent_condition: the parent condition under which the ChipExo data
            was collected
        - file: the path to the file containing the ChipExo data. The fields
            are: `chr`   `coord`  `YPD_Sig` `YPD_Ctrl` `YPD_log2Fold`
            `YPD_log2P` `ActiveConds`, where `chr` and `coord` are created
            from the original `Point` column, split on the `:` character

    Example usage:

    .. code-block:: python

        from callingcards.models import ChipExo_s3

        # get all ChipExo_s3 records
        all_records = ChipExo_s3.objects.all()
    """

    CONDITION_CHOICES = [('YPD', 'YPD')]

    # the TF which was overexpressed. This foreign keys to
    # the gene table
    regulator = models.ForeignKey(
        'Regulator',
        models.CASCADE,
        related_name='chipexo_s3_regulator',
        db_index=True)
    chipexo_id = models.CharField(
        max_length=15,
        null=False,
        blank=False)
    replicate = models.PositiveSmallIntegerField(
        null=False,
        blank=False)
    accession = models.CharField(
        max_length=11,
        null=False,
        blank=False)
    sra_accession = models.CharField(
        max_length=11,
        null=False,
        blank=False)
    condition = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=CONDITION_CHOICES)
    parent_condition = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=CONDITION_CHOICES)
    sig_count = models.PositiveSmallIntegerField(
        null=False,
        blank=False)
    control_count = models.PositiveSmallIntegerField(
        null=False,
        blank=False)
    sig_fraction = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=6,
        decimal_places=5)
    sig_ctrl_scaling = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=6,
        decimal_places=5)
    file = models.FileField(upload_to='temp',
                            help_text="The allevents tsv file from the "
                            "the Pugh yeastepigenome site. The file will "
                            "have the headers `chr`   `coord`  `YPD_Sig` "
                            "`YPD_Ctrl` `YPD_log2Fold` `YPD_log2P` "
                            "`ActiveConds`")

    class Meta:
        managed = True
        db_table = 'chipexo_s3'

    def save(self, *args, **kwargs):
        # Store the old file path
        old_file_name = self.file.name if self.file else None
        super().save(*args, **kwargs)
        self.update_file_name('file', 'chipexo/chexmix', 'tsv.gz')
        new_file_name = self.file.name
        super().save(update_fields=['file'])
        # If the file name changed, delete the old file
        if old_file_name and old_file_name != new_file_name:
            default_storage.delete(old_file_name)


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
