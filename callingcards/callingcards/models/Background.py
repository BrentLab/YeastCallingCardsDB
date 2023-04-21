"""
.. module:: Background
   :synopsis: Model for storing background genomic regions.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-20

This module defines the `Background` model, which is used to store background
genomic regions. The model inherits from the `BaseModel` and
`GenomicCoordinatesMixin` classes, which provide fields for tracking the user
who uploaded the data, the date of uploading, and the last modification date
and user who made the modification, as well as genomic coordinates.
"""
from django.db import models  # pylint: disable=import-error # noqa # type: ignore

from .BaseModel import BaseModel
from .mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin


class Background(GenonomicCoordinatesMixin, BaseModel):
    """
    A model for storing background genomic regions.

    Inherits from the BaseModel and GenomicCoordinatesMixin classes,
    which provide common fields for tracking the user who uploaded the data,
    the date of uploading, and the last modification date and user who made
    the modification, as well as genomic coordinates.

    Fields:
        - chr: ForeignKey to the ChrMap model, representing the chromosome
          that the background region is on.
        - start: IntegerField, representing the start position of the
          background region.
        - end: IntegerField, representing the end position of the background
          region.
        - strand: CharField with a max length of 1, representing the strand
          that the background region is on.
        - depth: PositiveIntegerField, representing the depth of the background
          region.
        - source: CharField with a max length of 5, representing the source
          of the background region.
        - uploader: ForeignKey to the user model, representing the user who
          uploaded the data.
        - uploadDate: DateField, automatically set to the date the object was
          created.
        - modified: DateTimeField, automatically set to the current date and
          time when the object is updated. Note that this field is only
          updated when the object is saved using the save() method, not when
          using queryset.update().
        - modifiedBy: ForeignKey to the user model, representing the user who
          last modified the data.

    Example usage:

    .. code-block:: python

        from callingcards.models import Background

        # get all Background records
        all_backgrounds = Background.objects.all()

    """
    DSIR4 = 'dsir4'
    ADH1 = 'adh1'

    SOURCE_CHOICES = ((DSIR4, 'dsir4'),
                      (ADH1, 'adh1'))

    depth = models.PositiveIntegerField()
    source = models.CharField(
        max_length=5,
        choices=SOURCE_CHOICES)

    class Meta:
        managed = True
        db_table = 'background'
