"""
.. module:: PromoterRegions_s3
   :synopsis: Model for storing PromoterRegions data.

This table defines the promoter regions, stored by file
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.core.files.storage import default_storage
from django.dispatch import receiver
from .BaseModel import BaseModel
from .ChrMap import ChrMap
from .mixins.FileUploadWithIdMixin import FileUploadMixin

logger = logging.getLogger(__name__)


class PromoterRegions_s3(BaseModel, FileUploadMixin):
    """
    A model for storing PromoterRegions bed files

    Fields:
        - chr_format: The format, which must be a field in the ChrMap table,
            of the chromosome names
        - source: The source of the promoter regions. This is foreign keyed to
            the PromoterSource table
        - file: a bed6 format file, with column names, which describes a set
            of promoter regions. The `name` field contains a key to the
            Gene table ID to which this promoter region is associated

    Example usage:

    .. code-block:: python

        from callingcards.models import PromoterRegions_s3

        # get all PromoterRegions_s3 records
        all_records = PromoterRegions_s3.objects.all()
    """
    CHR_FORMAT_CHOICES = [
        (x.name, x.name) for x in ChrMap._meta.fields if x.name not in
        {'uploader', 'uploadDate', 'modified',
         'modifiedBy', 'seqlength', 'type'}]

    chr_format = models.CharField(max_length=25,
                                  choices=CHR_FORMAT_CHOICES,
                                  default='id',
                                  help_text="Format of the chromosome column "
                                  "This must be a field in the ChrMap table")
    source = models.ForeignKey(
        "PromoterRegionsSource",
        models.CASCADE,
        help_text="The source (name) of a given set of promoter regions. "
        "Foreign keyed to the PromoterSource table")

    file = models.FileField(upload_to='temp',
                            help_text="A bed file describing promoter "
                            "regions. The name field contains the Gene table "
                            "ID to which a given promoter region is "
                            "associated")

    def __str__(self) -> str:
        return (f'promoter_source:{self.source}')

    class Meta:
        managed = True
        db_table = 'promoterregions_s3'

    def save(self, *args, **kwargs):
        # Store the old file path
        old_file_name = self.file.name if self.file else None
        super().save(*args, **kwargs)
        self.update_file_name('file', 'promoter_regions', 'csv.gz')
        new_file_name = self.file.name
        super().save(update_fields=['file'])
        # If the file name changed, delete the old file
        if old_file_name and old_file_name != new_file_name:
            default_storage.delete(old_file_name)


@receiver(models.signals.post_delete, sender=PromoterRegions_s3)
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
