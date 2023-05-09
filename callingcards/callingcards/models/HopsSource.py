"""
.. module:: CallingCardsSig
   :synopsis: Model and related functions to store information regarding the 
   source of the Hops data. This is used to track the pipeline and pipeline
   version used to generate the data.

Store information regarding the Hops data processing in the database, eg
'nf-core/callingcards v1.0.0'

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-26
"""
import logging
from .BaseModel import BaseModel
from .mixins.ProvidenceMixin import ProvidenceMixin

logger = logging.getLogger(__name__)


class HopsSource(ProvidenceMixin, BaseModel):
    class Meta:
        db_table = 'hopssource'
        ordering = ['source']
        verbose_name = 'HopsSource'
        managed = True
