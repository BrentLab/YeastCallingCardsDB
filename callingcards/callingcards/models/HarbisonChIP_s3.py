"""
.. module:: HarbisonChIP_s3
   :synopsis: Model for storing HarbisonChIP data.

This module defines a table which stores the file paths to files containing
the Harbison ChIP data
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.dispatch import receiver
from .BaseModel import BaseModel
from .filepaths.harbisonchip_filepath import harbisonchip_filepath

logger = logging.getLogger(__name__)


class HarbisonChIP_s3(BaseModel):
    """
    A model for storing Harbison ChIP data from:
    http://younglab.wi.mit.edu/regulatory_code/GWLD.html

    Fields:

    Example usage:

    .. code-block:: python

        from callingcards.models import HarbisonChIP_s3

        # get all HarbisonChIP_s3 records
        all_records = HarbisonChIP_s3.objects.all()
    """

    CONDITION_CHOICES = [('YPD', 'YPD')]

    # the TF which was overexpressed. This foreign keys to
    # the gene table
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        related_name='harbisonchip_s3_tf',
        db_index=True)
    file = models.FileField(upload_to=harbisonchip_filepath,
                            help_text="")

    class Meta:
        managed = True
        db_table = 'harbisonchip_s3'


@receiver(models.signals.post_delete, sender=HarbisonChIP_s3)
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
