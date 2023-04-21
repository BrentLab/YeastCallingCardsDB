"""
.. module:: chr_map
   :synopsis: Module for the `ChrMap` model that stores chromosome mapping
              information for different genome assemblies.

This module defines the `ChrMap` model used to store the chromosome mapping
information for different genome assemblies, including the `refseq`, `igenomes`,
`ensembl`, `ucsc`, `mitra`, `seqlength`, `numbered`, and `chr` fields.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-21
"""
from django.db import models
from .BaseModel import BaseModel


class ChrMap(BaseModel):
    """
    A model for storing chromosome mapping information for different genome
    assemblies.

    Fields:
        - `refseq`: CharField with a max length of 12, representing the RefSeq
          identifier for a given chromosome.
        - `igenomes`: CharField with a max length of 12, representing the 
          iGenomes identifier for a given chromosome.
        - `ensembl`: CharField with a max length of 12, representing the 
          Ensembl identifier for a given chromosome.
        - `ucsc`: CharField with a max length of 12, representing the UCSC
          identifier for a given chromosome.
        - `mitra`: CharField with a max length of 15, representing the Mitra
          identifier for a given chromosome.
        - `seqlength`: PositiveIntegerField representing the sequence length of
          a given chromosome.
        - `numbered`: CharField with a max length of 12, representing the
          numbered identifier for a given chromosome.
        - `chr`: CharField with a max length of 12, representing the chromosome
          number or identifier.

    Example usage:

    .. code-block:: python

        from callingcards.models import ChrMap

        # get all ChrMap records
        all_maps = ChrMap.objects.all()

    """
    refseq = models.CharField(
        max_length=12)
    igenomes = models.CharField(
        max_length=12)
    ensembl = models.CharField(
        max_length=12)
    ucsc = models.CharField(
        max_length=12)
    mitra = models.CharField(
        max_length=15)
    seqlength = models.PositiveIntegerField()
    numbered = models.CharField(
        max_length=12
    )
    chr = models.CharField(
        max_length=12)

    class Meta:
        managed = True
        db_table = 'chr_map'
