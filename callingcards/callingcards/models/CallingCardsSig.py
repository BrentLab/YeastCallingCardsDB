"""
.. module:: CallingCardsSig
   :synopsis: Model and related functions to store significance data in the 
   form of files in the database.

Store significance data in the form of files in the database.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-26
"""
import logging
from django.db import models
from django.core.files.storage import default_storage
from .BaseModel import BaseModel
from .mixins.FileUploadWithIdMixin import FileUploadMixin

logger = logging.getLogger(__name__)


class CallingCardsSig(BaseModel, FileUploadMixin):
    experiment = models.ForeignKey('CCExperiment',
                                   on_delete=models.CASCADE)
    hops_source = models.ForeignKey('HopsSource',
                                    on_delete=models.CASCADE)
    background_source = models.ForeignKey('BackgroundSource',
                                          on_delete=models.CASCADE)
    promoter_source = models.ForeignKey('PromoterRegionsSource',
                                        on_delete=models.CASCADE)
    file = models.FileField(upload_to='temp',
                            help_text="A csv file containing significance "
                                      "data for a given experiment in a "
                                      "given background and set of promoter "
                                      "regions")
    notes = models.CharField(max_length=50, default='none')

    class Meta:
        db_table = 'callingcardssig'
        unique_together = (('experiment',
                            'hops_source',
                            'promoter_source',
                            'background_source'),)
        ordering = ['experiment',
                    'hops_source',
                    'promoter_source',
                    'background_source']
        verbose_name = 'CallingCardsSig'
        managed = True

    def save(self, *args, **kwargs):
        # Store the old file path
        old_file_name = self.file.name if self.file else None
        super().save(*args, **kwargs)
        self.update_file_name('file', 'callingcards/sig', 'csv.gz')
        new_file_name = self.file.name
        super().save(update_fields=['file'])
        # If the file name changed, delete the old file
        if old_file_name and old_file_name != new_file_name:
            default_storage.delete(old_file_name)
