"""
.. module:: kemmerentfko_s3
   :synopsis: Model for storing Kemmeren TFKO data in S3.

This module defines a table which stores the file paths to files containing
the Kemmeren TFKO data
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.dispatch import receiver
from .BaseModel import BaseModel
from .filepaths.kemmerentfko_filepath import kemmerentfko_filepath

logger = logging.getLogger(__name__)


class KemmerenTFKO_s3(BaseModel):
    """
    A model for storing Kemmeren TFKO data from:
    https://deleteome.holstegelab.nl/

    Fields:

    Example usage:

    .. code-block:: python

        from callingcards.models import kemmerentfko_s3

        # get all kemmerentfko_s3 records
        all_records = kemmerentfko_s3.objects.all()
    """
    REFERENCE_CHOICES = [("wt-matA", "wt-matA"),
                         ("wt", "wt")]
    
    # the regulator which was overexpressed. This foreign keys to
    # the gene table
    regulator = models.ForeignKey(
        'Regulator',
        models.PROTECT,
        related_name='kemmerentfko_s3_regulator',
        help_text="Kemmeren reference strain",
        db_index=True)
    reference = models.CharField(max_length=7,
                                 help_text="Kemmeren reference strain",
                                 choices=REFERENCE_CHOICES,
                                 db_index=True)
    file = models.FileField(upload_to=kemmerentfko_filepath,
                            help_text="")

    class Meta:
        managed = True
        db_table = 'kemmerentfko_s3'


@receiver(models.signals.post_delete, sender=KemmerenTFKO_s3)
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
