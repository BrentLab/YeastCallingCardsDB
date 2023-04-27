"""
.. module:: CallingCardsSig
   :synopsis: Model and related functions to store information regarding the 
   source of promoter regions in the database.

Store information regarding the source of promoter regions in the database.
This should include the name commonly used to refer to the promoter source 
(e.g. "yiming" or "not_orf"), the source of the promoter regions (preferably
a link to code which reconstructs the promoter regions), and any notes

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-26
"""
import logging
from .BaseModel import BaseModel
from .mixins.ProvidenceMixin import ProvidenceMixin

logger = logging.getLogger(__name__)


class PromoterRegionsSource(ProvidenceMixin, BaseModel):
    class Meta:
        db_table = 'promoterregionssource'
        #ordering = ['source']
        verbose_name = 'PromoterRegionsSource'
        managed = True