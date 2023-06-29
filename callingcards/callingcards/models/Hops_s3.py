import logging
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.dispatch import receiver
from .BaseModel import BaseModel
from .ChrMap import ChrMap
from .filepaths.qbed_filepath import qbed_filepath

logger = logging.getLogger(__name__)


class Hops_s3(BaseModel):
    """
    Store qbed file by experiment id 
    """
    CHR_FORMAT_CHOICES = [
        (x.name, x.name) for x in ChrMap._meta.fields if x.name not in
        {'uploader', 'uploadDate', 'modified', 'modifiedBy', 'seqlength'}]

    chr_format = models.CharField(max_length=25,
                                  choices=CHR_FORMAT_CHOICES,
                                  default='id')
    source = models.ForeignKey('HopsSource',
                               on_delete=models.CASCADE)
    experiment = models.ForeignKey('CCExperiment',
                                   on_delete=models.CASCADE)
    qbed = models.FileField(upload_to=qbed_filepath)
    genomic_hops = models.PositiveIntegerField(default=0)
    plasmid_hops = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=50, default='none')

    def __str__(self):
        return str(self.qbed)

    class Meta:
        db_table = 'hops_s3'


# Signals
# this is a post_delete signal. Hence, if the delete command is successful,
# the file will be deleted. If the delete command is successful, and for some
# reason the delete signal fails, it is possible to end up with files in S3
# which are not referenced by the database.
# upon inception, there did not exist any images which were not referenced. So,
# if unreferenced files are ever found, that should indicate that these files
# are erroneous and can be safely deleted
@receiver(models.signals.post_delete, sender=Hops_s3)
def remove_file_from_s3(sender, instance, using, **kwargs):
    # note that if the directory (and all subdirectories) are empty, the
    # directory will also be removed
    instance.qbed.delete(save=False)
