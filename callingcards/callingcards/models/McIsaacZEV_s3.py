"""
.. module:: mcisaac_zev_s3
   :synopsis: Model for storing McIsaac ZEV data.

This module defines the `McIsaacZEV_s3` model, which is used to store McIsaac ZEV
data along with the target gene and transcription factor. Data is stored as 
a file by tf, strain, date, restriction, mechanism, and time. The file is
stored in S3 and the path to the file is stored in the database.
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.core.files.storage import default_storage
from django.dispatch import receiver
from .BaseModel import BaseModel
from .mixins.FileUploadWithIdMixin import FileUploadMixin

logger = logging.getLogger(__name__)


class McIsaacZEV_s3(BaseModel, FileUploadMixin):
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
    RESTRICTION_CHOICES = [('P', 'P'),
                           ('M', 'M'),
                           ('N', 'N')]

    MECHANISM_CHOICES = [('ZEV', 'ZEV'),
                         ('GEV', 'GEV')]

    TIME_CHOICES = [('0', '0'),
                    ('2.5', '2.5'),
                    ('5', '5'),
                    ('7.5', '7.5'),
                    ('8', '8'),
                    ('10', '10'),
                    ('12.5', '12.5'),
                    ('15', '15'),
                    ('18', '18'),
                    ('20', '20'),
                    ('30', '30'),
                    ('45', '45'),
                    ('60', '60'),
                    ('90', '90'),
                    ('100', '100'),
                    ('120', '120'),
                    ('180', '180'),
                    ('290', '290')]

    # the TF which was overexpressed. This foreign keys to
    # the gene table
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='mcisaaczevs3_tf',
        db_index=True)
    strain = models.CharField(
        max_length=15,
        null=False,
        blank=False)
    date = models.DateField(
        null=False,
        blank=False)
    restriction = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        choices=RESTRICTION_CHOICES)
    mechanism = models.CharField(
        max_length=3,
        null=False,
        blank=False)
    time = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        choices=TIME_CHOICES)
    file = models.FileField(upload_to='temp',
                            help_text="Path to the McIsaac ZEV csv")

    class Meta:
        managed = True
        db_table = 'mcisaaczev_s3'

    def save(self, *args, **kwargs):
        # Store the old file path
        old_file_name = self.file.name if self.file else None
        super().save(*args, **kwargs)
        self.update_file_name('file', 'mcisaacZEV', 'csv.gz')
        new_file_name = self.file.name
        super().save(update_fields=['file'])
        # If the file name changed, delete the old file
        if old_file_name and old_file_name != new_file_name:
            default_storage.delete(old_file_name)

# Signals
# this is a post_delete signal. Hence, if the delete command is successful,
# the file will be deleted. If the delete command is successful, and for some
# reason the delete signal fails, it is possible to end up with files in S3
# which are not referenced by the database.
# upon inception, there did not exist any images which were not referenced. So,
# if unreferenced files are ever found, that should indicate that these files
# are erroneous and can be safely deleted


@receiver(models.signals.post_delete, sender=McIsaacZEV_s3)
def remove_file_from_s3(sender, instance, using, **kwargs):
    # note that if the directory (and all subdirectories) are empty, the
    # directory will also be removed
    instance.file.delete(save=False)
