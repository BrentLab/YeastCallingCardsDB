"""
.. module:: gene
   :synopsis: Module for the `Gene` model that stores genomic coordinates and
              annotations for genes.

This module defines the `Gene` model used to store genomic coordinates and
annotations for genes, including the `chr`, `start`, `end`, `strand`, `type`,
`gene_biotype`, `locus_tag`, `gene`, `source`, `alias`, and `note` fields.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-21
"""
from django.db import models
from .BaseModel import BaseModel
from .mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin


class Gene(GenonomicCoordinatesMixin, BaseModel):
    """
    A model for storing genomic coordinates and annotations for genes.

    Fields:
        - `chr`: ForeignKey to the `ChrMap` model, representing the chromosome
          that the gene is located on.
        - `start`: PositiveIntegerField representing the starting genomic
          coordinate of the gene.
        - `end`: IntegerField representing the ending genomic coordinate of
          the gene.
        - `strand`: CharField with a max length of 1, representing the strand
          of the gene.
        - `type`: CharField with a max length of 30, representing the type of
          the gene.
        - `gene_biotype`: CharField with a max length of 20, representing the
          biotype of the gene.
        - `locus_tag`: CharField with a max length of 20 and a unique
          constraint, representing the locus tag of the gene.
        - `gene`: CharField with a max length of 20, representing the gene
          name.
        - `source`: CharField with a max length of 50, representing the source
          of the gene information.
        - `alias`: CharField with a max length of 150, representing the alias
          of the gene.
        - `note`: CharField with a max length of 1000, representing any notes
          about the gene.

    Example usage:

    .. code-block:: python

        from callingcards.models import Gene

        # get all Gene records
        all_genes = Gene.objects.all()

    """
    type = models.CharField(
        max_length=30,
        default='unknown'
    )
    gene_biotype = models.CharField(
        max_length=20,
        default='unknown'
    )
    # note: in the save method below, a unique integer is appended to the
    # default value if the this field is left blank on input
    locus_tag = models.CharField(
        unique=True,
        max_length=20,
        default='unknown')
    # note: in the save method below, a unique integer is appended to the
    # default value if the this field is left blank on input
    gene = models.CharField(
        max_length=20,
        default='unknown')
    source = models.CharField(
        max_length=50)
    # note: in the save method below, a unique integer is appended to the
    # default value if the this field is left blank on input
    alias = models.CharField(
        max_length=150,
        default='unknown')
    note = models.CharField(
        max_length=1000,
        default='none')

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate a unique
        integer to append to the `locus_tag`, `gene`, and `alias` fields if
        they are left blank on input.
        """
        # Get the maximum value of the auto-incremented field in the table
        max_id = Gene.objects.aggregate(models.Max('id'))['id__max'] or 0
        # Check if the systematic field has the default value
        if self.locus_tag == 'unknown':
            self.locus_tag = f'unknown_{max_id + 1}'

        if self.gene == 'unknown':
            self.gene = f'unknown_{max_id + 1}'

        if self.alias == 'unknown':
            self.alias = f'unknown_{max_id + 1}'

        super().save(*args, **kwargs)
      
    def __str__(self):
        """
        Returns a string representation of the `Gene` model.
        """
        return f'{self.gene}({self.locus_tag}; GeneID: {self.id}'  # pylint: disable=no-member # noqa

    class Meta:
        managed = True
        db_table = 'gene'
