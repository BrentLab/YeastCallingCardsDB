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
from .BaseModel import BaseModel
from .filepaths.cc_replicate_sig_filepath import cc_replicate_sig_filepath

logger = logging.getLogger(__name__)


class CallingCardsSig(BaseModel):
    experiment = models.ForeignKey('CCExperiment',
                                   on_delete=models.CASCADE)
    qbed_source = models.ForeignKey('HopsSource',
                                    on_delete=models.CASCADE)
    background_source = models.ForeignKey('BackgroundSource',
                                          on_delete=models.CASCADE)
    promoter_source = models.ForeignKey('PromoterRegionsSource',
                                        on_delete=models.CASCADE)
    file = models.FileField(upload_to=cc_replicate_sig_filepath)
    notes = models.CharField(max_length=50, default='none')

    class Meta:
        db_table = 'callingcardssig'
        unique_together = (('experiment', 
                            'promoter_source', 
                            'background_source'),)
        ordering = ['experiment', 
                    'promoter_source', 
                    'background_source']
        verbose_name = 'CallingCardsSig'
        managed = True
