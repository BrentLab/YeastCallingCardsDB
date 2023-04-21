"""
.. module:: hops
   :synopsis: Module for the `Hops` model that stores HOPS data.

This module defines the `Hops` model used to store HOPS data, including the
`chr`, `start`, `end`, `strand`, `depth`, and `experiment` fields.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-21
"""
from django.db import models
from .BaseModel import BaseModel
from .mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin


class Hops(GenonomicCoordinatesMixin, BaseModel):
    """
    A model for storing HOPS data.

    Fields:
        - `chr`: ForeignKey to the `ChrMap` model, representing the chromosome
          where the HOPS data is located.
        - `start`: IntegerField representing the start coordinate of the HOPS
          data on the chromosome.
        - `end`: IntegerField representing the end coordinate of the HOPS data
          on the chromosome.
        - `strand`: CharField with a max length of 1 and choices of
          `'+'`, `'-'`,
          or `'.'`, representing the strand of the HOPS data.
        - `depth`: PositiveIntegerField representing the depth of coverage of
          the HOPS data.
        - `experiment`: ForeignKey to the `CCExperiment` model, representing
          the experiment associated with the HOPS data.

    Example usage:

    .. code-block:: python

        from callingcards.models import Hops

        # get all Hops records
        all_hops = Hops.objects.all()

    """
    depth = models.PositiveIntegerField()
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE,
        db_index=True)

    class Meta:
        managed = True
        db_table = 'hops'
