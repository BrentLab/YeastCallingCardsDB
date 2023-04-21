
"""
.. module:: promoter_regions
   :synopsis: Model for storing information about promoter regions.

This module defines the `PromoterRegions` model, which represents a genomic
region upstream of a gene that is associated with the gene's promoter. This model
inherits from the `GenonomicCoordinatesMixin` class, which provides fields for
storing genomic coordinates.

.. seealso:: `GenonomicCoordinatesMixin`

.. author:: Chase Mateusiak
.. date:: 2023-04-20
"""
from django.db import models
from django.core.validators import MaxValueValidator
from .BaseModel import BaseModel
from .mixins.GenomicCoordinatesMixin import GenonomicCoordinatesMixin


class PromoterRegionsQuerySet(models.QuerySet):
    """
    A queryset for the PromoterRegions model that provides an optimized method
    for retrieving promoter regions and their associated targets.

    Example usage:

    .. code-block:: python

        from callingcards.models import PromoterRegionsQuerySet

        # get all promoter regions and their associated targets
        promoter_targets = PromoterRegions.objects.targets()
    """

    def targets(self):
        """return a Queryset with the associated targets of a given promoter

        Returns:
            QuerySet: a QuerySet containing the promoter regions and their
                      associated targets. This method selects related 
                      'associated_feature' and annotates the resulting 
                      QuerySet with additional fields, including promoter id, 
                      target gene id, target locus tag, target gene, 
                      and source.
        """
        return self\
            .select_related(
                'associated_feature',
            )\
            .annotate(
                promoter_id=models.F('id'),
                target_gene_id=models.F('associated_feature_id'),
                target_locus_tag=models.F('associated_feature__locus_tag'),
                target_gene=models.F('associated_feature__gene'))\
            .values('promoter_id', 'target_gene_id', 'target_locus_tag',
                    'target_gene', 'source')

    def calling_cards(self, experiment_id, background_source,
                      consider_strand=False, pseudocount=0.2):
        # Calculate total_expression_hops and total_background_hops
        total_expression_hops = Hops.objects\
            .filter(experiment_id=experiment_id).count()
        total_background_hops = Background.objects\
            .filter(source=background_source).count()

        # Filter and annotate depending on whether the strand should
        # be considered
        if consider_strand:
            strand_condition = Q(strand=F('associated_feature__strand'))
        else:
            strand_condition = Q()

        expression_hops = Hops.objects.filter(
            chr=F('associated_feature__chr'),
            start__gte=F('associated_feature__start'),
            end__lte=F('associated_feature__end'),
            experiment_id=experiment_id,
            **strand_condition
        ).annotate(
            promoter_id=F('associated_feature__genepromoter'),
        ).values('promoter_id').annotate(
            expression_hops=Count('*'),
        )

        background_hops = Background.objects.filter(
            chr=F('associated_feature__chr'),
            start__gte=F('associated_feature__start'),
            end__lte=F('associated_feature__end'),
            source=background_source,
            **strand_condition
        ).annotate(
            promoter_id=F('associated_feature__genepromoter'),
        ).values('promoter_id').annotate(
            background_hops=Count('*'),
        )

        return self.annotate(
            expression_hops=Subquery(expression_hops
                                     .values('expression_hops')[:1]),
            background_hops=Subquery(background_hops
                                     .values('background_hops')[:1]),
        ).annotate(
            effect=compute_cc_effect(
                F('expression_hops'),
                total_expression_hops,
                F('background_hops'),
                total_background_hops,
                pseudocount
            ),
        )


class PromoterRegions(GenonomicCoordinatesMixin,
                      BaseModel):
    """
    A model representing a genomic region upstream of a gene that is associated
    with the gene's promoter.

    Fields:
        - chr: ForeignKey to the `ChrMap` model, representing the chromosome on
          which the promoter region is located.
        - start: PositiveIntegerField, representing the starting position of
          the promoter region.
        - end: PositiveIntegerField, representing the ending position of the
          promoter region.
        - strand: CharField with a max length of 1, representing the strand of
          the promoter region.
        - associated_feature: ForeignKey to the `gene` model, representing the
          gene that is associated with the promoter region.
        - score: PositiveSmallIntegerField, representing a score associated
          with the promoter region.
        - source: CharField with a max length of 10, representing the source of
          the promoter region.

    Example usage:

    .. code-block:: python

        from callingcards.models import PromoterRegions

        # get all PromoterRegions records
        all_promoter_regions = PromoterRegions.objects.all()

    """

    objects = PromoterRegionsQuerySet.as_manager()

    NOT_ORF = 'not_orf'
    YIMING = 'yiming'

    SOURCE_CHOICES = ((NOT_ORF, 'not_orf'),
                      (YIMING, 'yiming'))

    associated_feature = models.ForeignKey(
        'gene',
        models.PROTECT,
        db_index=True,
        related_name='genepromoter')
    score = models.PositiveSmallIntegerField(
        default=100,
        validators=[MaxValueValidator(100)]
    )
    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES
    )

    class Meta:
        managed = True
        db_table = 'promoter_regions'
