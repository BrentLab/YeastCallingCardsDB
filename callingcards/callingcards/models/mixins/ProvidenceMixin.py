"""
.. module:: ProvidenceMixin
   :synopsis: A mixin to store providence information, eg for the 
   promoterregions or background models

Store information regarding the providence of data.
This should include the name (source field) commonly used to refer to the
promoter source (e.g. "yiming" or "not_orf"), the source of the promoter
regions (preferably a link to code which reconstructs the promoter regions),
and any notes

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-26
"""
import logging
from django.db import models

logger = logging.getLogger(__name__)


class ProvidenceMixin(models.Model):
    source = models.CharField(primary_key=True,
                                  max_length=100)
    providence = models.CharField(max_length=100, default='none')
    notes = models.CharField(max_length=500, default='none')

    class Meta:
        abstract = True
