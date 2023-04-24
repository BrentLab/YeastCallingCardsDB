"""
.. module:: calligncards_with_metrics
   :synopsis: Module for calling cards quantification functions.

This module contains functions for calculating various statistical values
related to the analysis of Calling Cards data. It includes functions for
computing Calling Cards effect (enrichment), Poisson p-value, and
hypergeometric p-value, as well as a function for processing and aggregating
data from multiple sources to obtain these values.

Functions
---------
- callingcards_with_metrics
- calling_cards_effect
- poisson_pval
- hypergeom_pval

.. author:: Chase Mateusiak
.. date:: 2023-04-23
"""

import logging
import time

from django.db.models import Q, Count
import scipy.stats as scistat
import pandas as pd

from ..models import (PromoterRegions, Hops, Background)
from ..filters import PromoterRegionsFilter, HopsFilter, BackgroundFilter

logger = logging.getLogger(__name__)


def callingcards_with_metrics(query_params_dict: dict) -> pd.DataFrame:
    """
    Compute metrics for promoter regions in a set of Calling Card experiments
    using filtered PromoterRegions, Hops, and Background querysets.

    :param query_params_dict: A dictionary containing filter parameters for
        PromoterRegions, Hops, and Background querysets.
    :type query_params_dict: dict
    :return: A DataFrame containing metrics for each promoter region,
        experiment, and background source, including effect, Poisson p-value,
        and hypergeometric p-value. If outside_data is True, the following
        changes are made: the expression_effect, expression_pval and 
        expression_source are added, and by default the CallingCards poisson 
        pvalue is transformed to 'binding_signal'. the 'experiment' column is 
        used to denote the source of the binding_data.
    :rtype: pandas.DataFrame

    The input `query_params_dict` may contain fields which are in the filter
    parameters for the PromoterRegions, Hops, and Background model filters.

    Example filter parameters in `query_params_dict` may include:

    - 'promoter_source': 'yiming
    - 'experiment_id': 75
    - 'background_source': 'adh1'
    - 'consider_strand': False
    """

    logging.debug(query_params_dict)

    # filter the PromoterRegions model objects
    filtered_promoters = PromoterRegionsFilter(
        query_params_dict,
        queryset=PromoterRegions.objects.all())

    # filter the Hops (calling cards experiments) model objects
    filtered_experiment = HopsFilter(
        query_params_dict,
        queryset=Hops.objects.all())

    # Group by the experiment_id
    # count the number of records per group
    # and remove the default ordering, if any
    unique_experiment_counts = (
        filtered_experiment.qs
        .values('experiment_id')
        .annotate(record_count=Count('id'))
        .order_by()
    )
    # Convert the result to a dictionary with experiment_id
    # as key and record_count as value
    experiment_counts_dict = {entry['experiment_id']:
                              entry['record_count'] for
                              entry in unique_experiment_counts}

    # filter the Background model objects
    filtered_background = BackgroundFilter(
        query_params_dict,
        queryset=Background.objects.all())

    # Group by the experiment_id
    # count the number of records per group
    # and remove the default ordering, if any
    unique_background_counts = (
        filtered_background.qs
        .values('source')
        .annotate(record_count=Count('id'))
        .order_by()
    )
    # Convert the result to a dictionary with experiment_id
    # as key and record_count as value
    background_counts_dict = {entry['source']:
                              entry['record_count'] for
                              entry in unique_background_counts}

    # by default, False
    consider_strand = bool(query_params_dict.get('consider_strand', False))

    # iterate over the filtered PromoterRegions records. For each record,
    # iterate over the set of experiments and count the number over hops
    # over that promoter region. Do the same for each background source.
    # Then, calculate the enrichment score for each promoter region
    results = []
    promoter_queryset = filtered_promoters.qs
    start_time = time.time()
    for promoter_region in promoter_queryset:
        # get the number of hops for each experiment over this promoter
        experiment_hops_list = []
        for experiment, experiment_total_hops in \
                experiment_counts_dict.items():
            experiment_hops = filtered_experiment.qs.filter(
                chr_id=promoter_region.chr_id,
                start__gte=promoter_region.start,
                start__lte=promoter_region.end,
                experiment_id=experiment)

            if consider_strand and promoter_region.strand != "*":
                experiment_hops = experiment_hops.filter(
                    Q(strand=promoter_region.strand) |
                    Q(strand="*"))

            # record experiment data
            experiment_hops_list.append(
                {
                    'promoter_id': promoter_region.id,
                    'experiment_id': experiment,
                    'experiment_hops': experiment_hops.count(),
                    'experiment_total_hops': experiment_total_hops
                }
            )
        # get the number of hops for each background source over this promoter
        background_hops_list = []
        for background_source, background_total_hops in \
                background_counts_dict.items():
            background_hops = filtered_background.qs.filter(
                chr_id=promoter_region.chr_id,
                start__gte=promoter_region.start,
                start__lte=promoter_region.end,
                source=background_source)

            if consider_strand and promoter_region.strand != "*":
                background_hops = background_hops.filter(
                    Q(strand=promoter_region.strand) |
                    Q(strand="*"))

            # record background data
            background_hops_list.append(
                {
                    'promoter_id': promoter_region.id,
                    'background_source': background_source,
                    'background_hops': background_hops.count(),
                    'background_total_hops': background_total_hops
                }
            )
        # for each experiment ...
        for experiment_hops_dict in experiment_hops_list:
            # for each background ...
            for background_hops_dict in background_hops_list:
                # record the results
                results.append(
                    {
                        'promoter_id': promoter_region.id,
                        'target_gene_id': promoter_region.associated_feature_id,
                        'experiment_id': experiment_hops_dict['experiment_id'],
                        'background_source':
                        background_hops_dict['background_source'],
                        'promoter_source': promoter_region.source,
                        'background_total_hops':
                        background_hops_dict['background_total_hops'],
                        'experiment_total_hops':
                        experiment_hops_dict['experiment_total_hops'],
                        'background_hops':
                        background_hops_dict['background_hops'],
                        'experiment_hops':
                        experiment_hops_dict['experiment_hops'],
                        'callingcards_enrichment': enrichment(
                            background_hops_dict['background_total_hops'],
                            experiment_hops_dict['experiment_total_hops'],
                            background_hops_dict['background_hops'],
                            experiment_hops_dict['experiment_hops'],
                            query_params_dict.get('pseudo_count', 0.2)),
                        'poisson_pval': poisson_pval(
                            background_hops_dict['background_total_hops'],
                            experiment_hops_dict['experiment_total_hops'],
                            background_hops_dict['background_hops'],
                            experiment_hops_dict['experiment_hops'],
                            query_params_dict.get('pseudo_count', 0.2)),
                        'hypergeometric_pval': hypergeom_pval(
                            background_hops_dict['background_total_hops'],
                            experiment_hops_dict['experiment_total_hops'],
                            background_hops_dict['background_hops'],
                            experiment_hops_dict['experiment_hops']),
                    }
                )

    logger.info('Time to process %s promoters: %s',
                len(promoter_queryset), time.time() - start_time)

    result_df = pd.DataFrame.from_dict(results)

    return result_df


def enrichment(total_background_hops: int,
               total_experiment_hops: int,
               background_hops: int,
               experiment_hops: int,
               pseudocount: float = 1e-10):
    """
    Compute the Calling Cards effect (enrichment) for the given hops counts.

    :param total_background_hops: Total number of hops in the background.
    :type total_background_hops: int
    :param total_experiment_hops: Total number of hops in the experiment.
    :type total_experiment_hops: int
    :param background_hops: Number of hops in the background region.
    :type background_hops: int
    :param experiment_hops: Number of hops in the experiment region.
    :type experiment_hops: int
    :param pseudocount: A small constant to avoid division by zero. 
        Default is 0.2.
    :type pseudocount: float
    :return: The Calling Cards effect (enrichment) value.
    :rtype: float
    """

    numerator = (experiment_hops / (total_experiment_hops + pseudocount))
    denominator = (background_hops / (total_background_hops + pseudocount))

    return (numerator / (denominator+pseudocount))


def poisson_pval(total_background_hops: int,
                 total_experiment_hops: int,
                 background_hops: int,
                 experiment_hops: int,
                 pseudocount: float = 1e-10) -> float:
    """
    Compute the Poisson p-value for the given hops counts.

    :param total_background_hops: Total number of hops in the background.
    :type total_background_hops: int
    :param total_experiment_hops: Total number of hops in the experiment.
    :type total_experiment_hops: int
    :param background_hops: Number of hops in the background promoter region.
    :type background_hops: int
    :param experiment_hops: Number of hops in the experiment promoter region.
    :type experiment_hops: int
    :param pseudocount: A small constant to avoid division by zero. 
        Default is 0.2.
    :type pseudocount: float
    :return: The Poisson p-value.
    :rtype: float
    """
    # check input
    if total_background_hops < 0 or not isinstance(total_background_hops, int):
        raise ValueError(('total_background_hops must '
                          'be a non-negative integer'))
    if total_experiment_hops < 0 or not isinstance(total_experiment_hops, int):
        raise ValueError(('total_experiment_hops must '
                          'be a non-negative integer'))
    if background_hops < 0 or not isinstance(background_hops, int):
        raise ValueError('background_hops must be a non-negative integer')
    if experiment_hops < 0 or not isinstance(experiment_hops, int):
        raise ValueError('experiment_hops must be a non-negative integer')

    hop_ratio = total_experiment_hops / (total_background_hops+pseudocount)
    # expected number of hops in the promoter region
    mu = (background_hops * hop_ratio) + pseudocount
    # random variable -- observed hops in the promoter region
    x = experiment_hops + pseudocount

    pval = 1 - scistat.poisson.cdf(x, mu)

    return pval


def hypergeom_pval(total_background_hops: int,
                   total_experiment_hops: int,
                   background_hops: int,
                   experiment_hops: int) -> float:
    """
    Compute the hypergeometric p-value for the given hops counts.

    :param total_background_hops: Total number of hops in the background.
    :type total_background_hops: int
    :param total_experiment_hops: Total number of hops in the experiment.
    :type total_experiment_hops: int
    :param background_hops: Number of hops in the background promoter region.
    :type background_hops: int
    :param experiment_hops: Number of hops in the experiment promoter region.
    :type experiment_hops: int
    :return: The hypergeometric p-value.
    :rtype: float
    """
    # check input
    if total_background_hops < 0 or not isinstance(total_background_hops, int):
        raise ValueError(('total_background_hops must '
                          'be a non-negative integer'))
    if total_experiment_hops < 0 or not isinstance(total_experiment_hops, int):
        raise ValueError(('total_experiment_hops must '
                          'be a non-negative integer'))
    if background_hops < 0 or not isinstance(background_hops, int):
        raise ValueError('background_hops must be a non-negative integer')
    if experiment_hops < 0 or not isinstance(experiment_hops, int):
        raise ValueError('experiment_hops must be a non-negative integer')

    # total number of objects (hops) in the bag (promoter region)
    M = total_background_hops + total_experiment_hops
    # if M is 0, the hypergeometric distribution is undefined
    # (there is no bag), so return 1
    if M < 1:
        return 1
    # number of 'success' objects in the population (experiment hops)
    n = total_experiment_hops
    # sample size (total hops drawn drawn from the bag)
    N = background_hops + experiment_hops
    # if N is 0, the hypergeometric distribution is undefined
    # (there is no sample), so return 1
    if N < 1:
        return 1
    # number of 'success' objects (experiment hops).
    # since we're interested in the chance of drawing a number of
    # experiment hops equal to or greater than the observed number,
    # we subtract 1 from the observed number in the CDF calculation.
    # Subtracting the result from 1 yields the right tailed p-value
    x = max((experiment_hops - 1), 0)

    pval = 1 - scistat.hypergeom.cdf(x, M, n, N)

    return pval
