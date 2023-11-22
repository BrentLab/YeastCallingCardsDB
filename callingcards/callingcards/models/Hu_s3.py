"""
.. module:: Hu_s3
   :synopsis: Model for storing Hu/Reimand-reprocessed data.

This module defines a table which stores the file paths to files containing
the Hu/Reimand-reprocessed data
"""
import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.dispatch import receiver
from .BaseModel import BaseModel
from .filepaths.hu_filepath import hu_filepath

logger = logging.getLogger(__name__)


class Hu_s3(BaseModel):
    """
    A model for storing Hu/Reimand-reprocessed data from:
    https://pubmed.ncbi.nlm.nih.gov/20385592/

    Fields:

    Example usage:

    .. code-block:: python

        from callingcards.models import Hu_s3

        # get all Hu_s3 records
        all_records = Hu_s3.objects.all()
    """
    regulator = models.ForeignKey(
        'Regulator',
        models.PROTECT,
        related_name='hu_s3_regulator',
        db_index=True)
    file = models.FileField(upload_to=hu_filepath,
                            help_text="A gziped csv with fields: "
                            "`gene_id`, 'effect' and 'pval'")

    class Meta:
        managed = True
        db_table = 'hu_s3'


@receiver(models.signals.post_delete, sender=Hu_s3)
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
