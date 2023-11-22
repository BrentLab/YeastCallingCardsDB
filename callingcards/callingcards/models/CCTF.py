"""
.. module:: CCTF
   :synopsis: Model for storing a list of transcription factors interrogated
              with calling cards.

.. moduleauthor:: Chase Mateusiak
.. date:: 2023-04-20

This module defines the `CCTF` model, which is used to store a list of the
transcription factors interrogated with calling cards.
"""
from django.db import models
from .BaseModel import BaseModel


class CCTFQuerySet(models.QuerySet):
    def tf_list(self):
        return self\
            .select_related(
                'tf',
            )\
            .annotate(   
                tf_locus_tag=models.F('tf__locus_tag'),
                tf_gene=models.F('tf__gene'),
            )\
            .values('tf_id', 'tf_locus_tag', 'tf_gene')


class CCTF(BaseModel):
    """This table is used to store a list of the transcription factors
    interrogated with calling cards.

    Inherits from the BaseModel class, which provides common fields for
    tracking the user who uploaded the data, the date of uploading, and the
    last modification date and user who made the modification.

    Fields:
        - tf: ForeignKey to the Gene model, representing the gene that the
        transcription factor is associated with.
        - strain: CharField with a max length of 20, representing the strain
        that the transcription factor is being interrogated in.
        - under_development: BooleanField, representing whether the calling
        card experiment for this transcription factor is still under
        development.
        - notes: CharField with a max length of 50, representing any notes
        about the transcription factor or calling card experiment.

    Example usage:

    .. code-block:: python


        from callingcards.models import CCTF

        # get all CCTF records
        all_cctfs = CCTF.objects.all()
    """
    objects = CCTFQuerySet.as_manager()

    # regulator = models.ForeignKey(
    #     'Regulator',
    #     models.CASCADE,
    #     db_index=True)
    
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT,
        db_index=True)
    strain = models.CharField(
        max_length=20,
        default='unknown'
    )
    under_development = models.BooleanField(
        default=False)
    notes = models.CharField(
        max_length=50,
        default='none'
    )

    def __str__(self):
        return str(self.tf) + '_' + str(self.id)  # pylint: disable=no-member

    class Meta:
        managed = True
        db_table = 'cc_tf'
