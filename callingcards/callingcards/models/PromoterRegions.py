
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
from django.db.models import F, Count
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

        :return: A QuerySet containing the promoter regions and their
                associated targets. This method selects related 
                'associated_feature' and annotates the resulting 
                QuerySet with additional fields, including promoter id, 
                target gene id, target locus tag, target gene, 
                and source.
        :rtype: QuerySet
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

    def calling_cards_experiment(self,
                                 tf_id: int = None,
                                 tf_locus_tag: str = None,
                                 tf_gene: str = None,
                                 experiment_id: int = None,
                                 experiment_batch: str = None,
                                 promoter_source: str = None,
                                 consider_strand: bool = False,
                                 **kwargs) -> models.QuerySet:  # noqa
        """return a Queryset with the associated targets of a given promoter

        This method creates a QuerySet for experiment hops by filtering the 
        :class:`PromoterRegions` based on the given ``promoter_source``, 
        ``experiment_id``, and the range of start positions. The queryset can
        also be filtered by strand if ``consider_strand`` is set to True.
        The result is a queryset that annotates the experiment hops count for
        each promoter.

        :param int experiment_id: The experiment id to filter hops records.
        :param str promoter_source: The source to filter promoter
        regions.
        :param bool consider_strand: Whether to consider the strand in the
        filtering process. Defaults to False.
        :param kwargs: Additional keyword argument which may be part of the 
        query parameters. Except for the paramters explicitely named above, 
        these are not used in the query.
        :return: A queryset of annotated experiment hops counts for each
        promoter.
        :rtype: QuerySet

        Example usage:

        .. code-block:: python

            from callingcards.models import PromoterRegionsQuerySet

            # get all promoter regions and their associated targets
            promoter_targets = PromoterRegions.objects\
              .calling_cards_experiment()

            .. seealso:: :py:meth:`calling_cards_background
        """
        experiment_hops = self\
            .filter(
                chr__hops__chr_id=F('chr'),
                chr__hops__start__gte=F('start'),
                chr__hops__start__lte=F('end'))

        if promoter_source:
            experiment_hops = experiment_hops\
                .filter(
                    source=promoter_source)

        # experiment_id will return a single experiment. The rest of these
        # filters will return multiple experiments. These should be viewed
        # as mutually exclusive.
        if experiment_id:
            experiment_hops = experiment_hops\
                .filter(
                    chr__hops__experiment_id=experiment_id)
        elif experiment_batch:
            experiment_hops = experiment_hops\
                .filter(
                    chr__hops__experiment__batch=experiment_batch)
        elif tf_id:
            experiment_hops = experiment_hops\
                .filter(
                    chr__hops__experiment__tf_id=tf_id)
        elif tf_locus_tag:
            experiment_hops = experiment_hops\
                .filter(
                    chr__hops__experiment__tf__locus_tag=tf_locus_tag)
        elif tf_gene:
            experiment_hops = experiment_hops\
                .filter(
                    chr__hops__experiment__tf__gene=tf_gene)

        if consider_strand:
            experiment_hops = experiment_hops\
                .filter(
                    chr__hops__strand=F('strand'))

        experiment_hops = experiment_hops\
            .annotate(
                promoter_id=F('id'))\
            .values(
                'promoter_id')\
            .annotate(
                experiment_hops=Count('chr__hops__id'),
                experiment_id=F('chr__hops__experiment_id'),
                promoter_source=F('source'),)

        return experiment_hops

    def calling_cards_background(self,
                                 background_source: str = None,
                                 promoter_source: str = None,
                                 consider_strand: bool = False):
        """Return a Queryset with the background hops count for each promoter.

        This method creates a QuerySet for background hops by filtering the
        :class:`PromoterRegions` based on the given ``promoter_source``, 
        ``background_source``, and the range of start positions. The queryset
        can also be filtered by strand if ``consider_strand`` is set to True.
        The result is a queryset that annotates the background hops count for
        each promoter.

        :param int tf_id: The transcription factor id to filter records.
        :param str tf_locus_tag: The transcription factor locus tag to filter records.
        :param str tf_gene: The transcription factor gene to filter records.
        :param int experiment_id: The experiment id to filter hops records.
        :param str experiment_batch: The experiment batch to filter records.
        :param str promoter_source: The source to filter promoter
        regions.
        :param bool consider_strand: Whether to consider the strand in the
        filtering process. Defaults to False.
        :return: A queryset of annotated experiment hops counts for each
        promoter.
        :rtype: QuerySet

        Example usage:

        .. code-block:: python

            from callingcards.models import PromoterRegionsQuerySet

            # get all promoter regions and their associated background hops
            promoter_background = PromoterRegions.objects\
                .calling_cards_background()

        .. seealso:: :py:meth:`calling_cards_experiment`
        """
        background_hops = self\
            .filter(
                chr__background__chr_id=F('chr'),
                chr__background__start__gte=F('start'),
                chr__background__start__lte=F('end'))
        
        if promoter_source:
            background_hops = background_hops\
                .filter(
                    source=promoter_source)
            
        if background_source:
            background_hops = background_hops\
                .filter(
                    chr__background__source=background_source)
        
        if consider_strand:
            background_hops = background_hops\
                .filter(
                    chr__background__strand=F('strand'))

        background_hops = background_hops\
            .annotate(
                promoter_id=F('id'))\
            .values(
                'promoter_id')\
            .annotate(
                background_hops=Count('chr__background__id'),
                background_source=F('chr__background__source'),
                promoter_source=F('source'),)

        return background_hops


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
