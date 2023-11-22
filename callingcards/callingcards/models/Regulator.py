"""
.. module:: Regulator
   :synopsis: Model for storing a list of transcription factors interrogated
              with calling cards.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-11-20

This module defines the `Regulator` model, which is used to store a list of the
transcription factors interrogated with calling cards.
"""
from django.db import models
from .BaseModel import BaseModel


class RegulatorQuerySet(models.QuerySet):
    def regulator_list(self):
        return self\
            .select_related(
                'regulator',
            )\
            .annotate(   
                regulator_locus_tag=models.F('regulator__locus_tag'),
                regulator_gene=models.F('regulator__gene'),
            )\
            .values('regulator_id', 'regulator_locus_tag', 'regulator_gene')


class Regulator(BaseModel):
    """This table is used to store the set of proteins on which an experiment
    has been performed. Eg, if a given locus tag is one of the overexpressed
    proteins in McIsaac or a TF in the callingcards set.

    Fields:
        - regulator: ForeignKey to the Gene model, representing the gene that
        the regulator.
        - strain: CharField with a max length of 20, representing the strain
        that the transcription factor is being interrogated in.
        - under_development: BooleanField, representing whether the calling
        card experiment for this transcription factor is still under
        development.
        - notes: CharField with a max length of 50, representing any notes
        about the transcription factor or calling card experiment.

    Example usage:

    .. code-block:: python


        from callingcards.models import Regulator

        # get all Regulator records
        all_regulators = Regulator.objects.all()
    """
    objects = RegulatorQuerySet.as_manager()

    regulator = models.ForeignKey(
        'Gene',
        models.PROTECT,
        db_index=True)
    notes = models.CharField(
        max_length=50,
        default='none'
    )

    def __str__(self):
        return str(self.regulator) + '_' + str(self.id)  # pylint: disable=no-member  # noqa

    class Meta:
        managed = True
        db_table = 'regulator'
