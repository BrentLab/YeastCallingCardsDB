"""
.. module:: Lab
   :synopsis: A model to store information about the lab that
      generated the data

Store information regarding the providence of data.
This should include the name (source field) commonly used to refer to the
promoter source (e.g. "yiming" or "not_orf"), the source of the promoter
regions (preferably a link to code which reconstructs the promoter regions),
and any notes

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-05-07
"""
import logging
from django.db import models
from .BaseModel import BaseModel

logger = logging.getLogger(__name__)


class Lab(BaseModel):
    lab = models.CharField(primary_key=True, max_length=25)
    notes = models.CharField(max_length=100, default='none')

    def __str__(self):
        return str(self.lab)

    class Meta:
        db_table = 'lab'
