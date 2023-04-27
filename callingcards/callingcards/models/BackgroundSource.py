"""
.. module:: CallingCardsSig
   :synopsis: Model and related functions to store information regarding the 
   source of the background data

Store information regarding the background data sources in the database, eg
'adh1'

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-26
"""
import logging
from .BaseModel import BaseModel
from .mixins.ProvidenceMixin import ProvidenceMixin

logger = logging.getLogger(__name__)


class BackgroundSource(ProvidenceMixin, BaseModel):
    class Meta:
        db_table = 'backgroundsource'
        #ordering = ['source']
        verbose_name = 'BackgroundSource'
        managed = True
