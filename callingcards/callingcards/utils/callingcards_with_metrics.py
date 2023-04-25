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
import itertools

from django.db.models import F, Count
import scipy.stats as scistat
import pandas as pd

from ..models import (PromoterRegions, Hops, Background)
from ..filters import PromoterRegionsFilter, HopsFilter, BackgroundFilter

logger = logging.getLogger(__name__)


def callingcards_with_metrics(query_params_dict: dict) -> pd.DataFrame:
    logging.debug(query_params_dict)

    # filter the PromoterRegions model objects
    filtered_promoters = PromoterRegionsFilter(
        query_params_dict,
        queryset=PromoterRegions.objects.all())

    filtered_promoters_df = pd.DataFrame.from_records(
        filtered_promoters.qs.values())

    # filter the Hops (calling cards experiments) model objects
    filtered_experiment_queryset = HopsFilter(
        query_params_dict,
        queryset=Hops.objects.all())\
        .qs\
        .select_related('experiment')

    # Group by the experiment_id
    # count the number of records per group
    # and remove the default ordering, if any
    unique_experiment_counts = (
        filtered_experiment_queryset
        .values('experiment_id')
        .annotate(record_count=Count('id'),
                  tf_id=F('experiment__tf__tf_id'),
                  experiment_batch=F('experiment__batch'),
                  experiment_replicate=F('experiment__batch_replicate'))
        .order_by()
    )
    # Convert the result to a dictionary with experiment_id
    # as key and record_count as value
    experiment_counts_dict = {
        entry['experiment_id']:
        {'experiment_total_hops': entry['record_count'],
         'tf_id': entry['tf_id'],
         'experiment_batch': entry['experiment_batch'],
         'experiment_replicate':
         entry['experiment_replicate']} for entry in unique_experiment_counts}

    # Convert experiment_counts_dict to a DataFrame
    filtered_experiment_df = pd.DataFrame\
        .from_records(filtered_experiment_queryset.values())

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
                              {'background_total_hops': entry['record_count']}
                              for entry in unique_background_counts}

    # Convert background hops data to a DataFrame
    filtered_background_df = pd.DataFrame\
        .from_records(filtered_background.qs.values())

    # by default, False
    consider_strand = bool(query_params_dict.get('consider_strand', False))

    # Convert experiment_counts_dict to a DataFrame
    experiment_counts_df = pd.DataFrame(
        experiment_counts_dict.values(),
        index=experiment_counts_dict.keys())
    experiment_counts_df.index.name = 'experiment_id'

    # Create a DataFrame with background_counts_dict
    background_counts_df = pd.DataFrame(
        background_counts_dict.values(),
        index=background_counts_dict.keys())
    background_counts_df.index.name = 'source'

    # Prepare filtered_experiment_df and filtered_background_df for merging
    filtered_experiment_df = filtered_experiment_df.merge(
        experiment_counts_df, on='experiment_id', how='left')

    # Prepare filtered_experiment_df and filtered_background_df for merging
    filtered_background_df = filtered_background_df.merge(
        background_counts_df, on='source', how='left')

    # Create a helper function to filter the data based on strand
    def filter_strand_data(hops_df, promoter_row, consider_strand):
        if consider_strand and promoter_row['strand'] != "*":
            return hops_df[
                (hops_df['strand'] == promoter_row['strand']) |
                (hops_df['strand'] == "*")
            ]
        else:
            return hops_df

    # Use apply to process each promoter row
    def process_promoter_row(promoter_row,
                             experiment_counts_df,
                             filtered_experiment_df,
                             background_counts_df,
                             filtered_background_df,
                             consider_strand):
        # Filter experiment and background hops based on promoter and strand
        filtered_exp_hops = filter_strand_data(
            filtered_experiment_df,
            promoter_row,
            consider_strand)

        filtered_bg_hops = filter_strand_data(
            filtered_background_df,
            promoter_row,
            consider_strand)

        # Calculate hops counts in the promoter region
        # note that counting on the chr_id field is arbitrary
        exp_hops_count = filtered_exp_hops[
            (filtered_exp_hops['chr_id'] == promoter_row['chr_id']) &
            (filtered_exp_hops['start'] >= promoter_row['start']) &
            (filtered_exp_hops['start'] <= promoter_row['end'])]\
            .groupby('experiment_id')\
            .agg({'experiment_total_hops': 'first', 'chr_id': 'count'})\
            .reset_index()\
            .rename(columns={'chr_id': 'experiment_hops'})

        # Perform an outer merge with experiment_counts_df
        exp_hops_count = experiment_counts_df.merge(
            exp_hops_count, on='experiment_id', how='left')

        exp_hops_count['experiment_total_hops'] = \
            exp_hops_count['experiment_total_hops_x']\
            .fillna(exp_hops_count['experiment_total_hops_y'])

        exp_hops_count.drop(['experiment_total_hops_x',
                             'experiment_total_hops_y'],
                            axis=1, inplace=True)

        # Fill missing values with 0 for experiment_hops
        exp_hops_count['experiment_hops'] = \
            exp_hops_count['experiment_hops'].fillna(0)

        # count the number of background hops
        bg_hops_count = filtered_bg_hops[
            (filtered_bg_hops['chr_id'] == promoter_row['chr_id']) &
            (filtered_bg_hops['start'] >= promoter_row['start']) &
            (filtered_bg_hops['start'] <= promoter_row['end'])]\
            .groupby('source')\
            .agg({'background_total_hops': 'first', 'chr_id': 'count'})\
            .reset_index()\
            .rename(columns={'chr_id': 'background_hops'})

        # Perform an outer merge with background_counts_df
        bg_hops_count = background_counts_df.merge(
            bg_hops_count, on='source', how='left')

        bg_hops_count['background_total_hops'] = \
            bg_hops_count['background_total_hops_x']\
            .fillna(bg_hops_count['background_total_hops_y'])

        bg_hops_count.drop(['background_total_hops_x',
                            'background_total_hops_y'],
                           axis=1, inplace=True)

        # Fill missing values with 0 for experiment_hops
        bg_hops_count['background_hops'] = \
            bg_hops_count['background_hops'].fillna(0)

        # Prepare data for merging
        exp_hops_count['key'] = 1
        bg_hops_count['key'] = 1
        merged_df = exp_hops_count\
            .merge(bg_hops_count, on='key')\
            .drop('key', axis=1)

        # Create a boolean mask for columns starting with "background" or "experiment"
        column_mask = merged_df.columns.str.endswith("hops")

        # Get the selected columns
        selected_columns = merged_df.columns[column_mask]

        # Convert each column to int individually
        for col in selected_columns:
            merged_df[col] = merged_df[col].astype(int)

        # Perform calculations using vectorized operations
        pseudo_count = query_params_dict.get('pseudo_count', 0.2)
        # Replace 'pseudo_count' with the actual value you are using
        result_df = merged_df\
            .apply(lambda row: metrics_wrapper(row, pseudo_count), axis=1)
        merged_df = pd.concat([merged_df, result_df], axis=1)

        return merged_df
    
    start_time = time.time()
    # Apply the process_promoter_row function to each row in filtered_promoters_df
    result_df = filtered_promoters_df.apply(process_promoter_row,
                                            axis=1,
                                            args=(experiment_counts_df,
                                                  filtered_experiment_df,
                                                  background_counts_df,
                                                  filtered_background_df,
                                                  consider_strand))
    logger.info("Time taken to process %s promoters: %s seconds",
                 len(filtered_promoters_df), time.time() - start_time)

    # Concatenate the resulting DataFrames and reset the index
    result_df = pd.concat(result_df.tolist(), ignore_index=True)

    return result_df


def metrics_wrapper(row: pd.Series, pseudocount: float = 0.2) -> pd.Series:
    background_total_hops = row['background_total_hops']
    experiment_total_hops = row['experiment_total_hops']
    background_hops = row['background_hops']
    experiment_hops = row['experiment_hops']

    callingcards_enrichment_res = enrichment(background_total_hops,
                                             experiment_total_hops,
                                             background_hops,
                                             experiment_hops,
                                             pseudocount)

    poisson_pval_res = poisson_pval(background_total_hops,
                                    experiment_total_hops,
                                    background_hops,
                                    experiment_hops,
                                    pseudocount)

    hypergeometric_pval_res = hypergeom_pval(background_total_hops,
                                             experiment_total_hops,
                                             background_hops,
                                             experiment_hops)

    return pd.Series({
        'callingcards_enrichment': callingcards_enrichment_res,
        'poisson_pval': poisson_pval_res,
        'hypergeometric_pval': hypergeometric_pval_res
    })


# def callingcards_with_metrics(query_params_dict: dict) -> pd.DataFrame:
#     """
#     Compute metrics for promoter regions in a set of Calling Card experiments
#     using filtered PromoterRegions, Hops, and Background querysets.

#     :param query_params_dict: A dictionary containing filter parameters for
#         PromoterRegions, Hops, and Background querysets.
#     :type query_params_dict: dict
#     :return: A DataFrame containing metrics for each promoter region,
#         experiment, and background source, including effect, Poisson p-value,
#         and hypergeometric p-value. If outside_data is True, the following
#         changes are made: the expression_effect, expression_pval and
#         expression_source are added, and by default the CallingCards poisson
#         pvalue is transformed to 'binding_signal'. the 'experiment' column is
#         used to denote the source of the binding_data.
#     :rtype: pandas.DataFrame

#     The input `query_params_dict` may contain fields which are in the filter
#     parameters for the PromoterRegions, Hops, and Background model filters.

#     Example filter parameters in `query_params_dict` may include:

#     - 'promoter_source': 'yiming
#     - 'experiment_id': 75
#     - 'background_source': 'adh1'
#     - 'consider_strand': False
#     """

#     logging.debug(query_params_dict)

#     # filter the PromoterRegions model objects
#     filtered_promoters = PromoterRegionsFilter(
#         query_params_dict,
#         queryset=PromoterRegions.objects.all())

#     filtered_promoters_df = pd.DataFrame.from_records(
#         filtered_promoters.qs.values())

#     # filter the Hops (calling cards experiments) model objects
#     filtered_experiment_queryset = HopsFilter(
#         query_params_dict,
#         queryset=Hops.objects.all())\
#         .qs\
#         .select_related('experiment')

#     # Group by the experiment_id
#     # count the number of records per group
#     # and remove the default ordering, if any
#     unique_experiment_counts = (
#         filtered_experiment_queryset
#         .values('experiment_id')
#         .annotate(record_count=Count('id'),
#                   tf_id=F('experiment__tf__tf_id'),
#                   experiment_batch=F('experiment__batch'),
#                   experiment_replicate=F('experiment__batch_replicate'))
#         .order_by()
#     )
#     # Convert the result to a dictionary with experiment_id
#     # as key and record_count as value
#     experiment_counts_dict = {
#         entry['experiment_id']:
#         {'total': entry['record_count'],
#          'tf_id': entry['tf_id'],
#          'experiment_batch': entry['experiment_batch'],
#          'experiment_replicate':
#          entry['experiment_replicate']} for entry in unique_experiment_counts}

#     # Convert experiment_counts_dict to a DataFrame
#     filtered_experiment_df = pd.DataFrame\
#         .from_records(filtered_experiment_queryset.values())

#     # filter the Background model objects
#     filtered_background = BackgroundFilter(
#         query_params_dict,
#         queryset=Background.objects.all())

#     # Group by the experiment_id
#     # count the number of records per group
#     # and remove the default ordering, if any
#     unique_background_counts = (
#         filtered_background.qs
#         .values('source')
#         .annotate(record_count=Count('id'))
#         .order_by()
#     )
#     # Convert the result to a dictionary with experiment_id
#     # as key and record_count as value
#     background_counts_dict = {entry['source']:
#                               entry['record_count'] for
#                               entry in unique_background_counts}

#     # Convert background hops data to a DataFrame
#     filtered_background_df = pd.DataFrame\
#         .from_records(filtered_background.qs.values())

#     # by default, False
#     consider_strand = bool(query_params_dict.get('consider_strand', False))

#     # iterate over the filtered PromoterRegions records. For each record,
#     # iterate over the set of experiments and count the number over hops
#     # over that promoter region. Do the same for each background source.
#     # Then, calculate the enrichment score for each promoter region
#     results = [None]*(len(filtered_promoters.qs)*len(experiment_counts_dict)*len(background_counts_dict))
#     promoter_queryset = filtered_promoters.qs
#     start_time = time.time()
#     index = 0
#     for promoter_region in promoter_queryset:
#         # get the number of hops for each experiment over this promoter
#         experiment_hops_list = []
#         for experiment, experiment_details_dict in experiment_counts_dict.items():
#             experiment_hops = filtered_experiment_df[
#                 (filtered_experiment_df['chr_id'] == promoter_region.chr_id) &
#                 (filtered_experiment_df['start'] >= promoter_region.start) &
#                 (filtered_experiment_df['start'] <= promoter_region.end) &
#                 (filtered_experiment_df['experiment_id'] == experiment)
#             ]

#             if consider_strand and promoter_region.strand != "*":
#                 experiment_hops = experiment_hops[
#                     (experiment_hops['strand'] == promoter_region.strand) |
#                     (experiment_hops['strand'] == "*")
#                 ]

#             # record experiment data
#             experiment_hops_list.append(
#                 {
#                     'promoter_id': promoter_region.id,
#                     'experiment_id': experiment,
#                     'experiment_batch': experiment_details_dict.get('experiment_batch'),
#                     'experiment_replicate': experiment_details_dict.get('experiment_replicate'),
#                     'tf_id': experiment_details_dict.get('tf_id'),
#                     'experiment_hops': len(experiment_hops),
#                     'experiment_total_hops': experiment_details_dict.get('total')
#                 }
#             )
#         # get the number of hops for each background source over this promoter
#         background_hops_list = []
#         for background_source, background_total_hops in \
#                 background_counts_dict.items():

#             background_hops = filtered_background_df[
#                 (filtered_background_df['chr_id'] == promoter_region.chr_id) &
#                 (filtered_background_df['start'] >= promoter_region.start) &
#                 (filtered_background_df['start'] <= promoter_region.end) &
#                 (filtered_background_df['source'] == background_source)
#             ]

#             if consider_strand and promoter_region.strand != "*":
#                 background_hops = background_hops[
#                     (background_hops['strand'] == promoter_region.strand) |
#                     (background_hops['strand'] == "*")
#                 ]

#             # record background data
#             background_hops_list.append(
#                 {
#                     'promoter_id': promoter_region.id,
#                     'background_source': background_source,
#                     'background_hops': len(background_hops),
#                     'background_total_hops': background_total_hops
#                 }
#             )

#         # create an iterable containing all possible pairs of experiment hops
#         # and background hops
#         experiment_background_pairs = itertools.product(
#             experiment_hops_list, background_hops_list)
#         # iterate over the pairs and compute the results
#         for experiment_hops_dict, background_hops_dict in \
#                 experiment_background_pairs:
#             # record the results
#             output_dict = {
#                 'promoter_id': promoter_region.id,
#                 'experiment_id': experiment_hops_dict['experiment_id'],
#                 'tf_id': experiment_hops_dict['tf_id'],
#                 'experiment_batch': experiment_hops_dict['experiment_batch'],
#                 'experiment_replicate': experiment_hops_dict['experiment_replicate'],
#                 'target_gene_id': promoter_region.associated_feature_id,
#                 'background_source':
#                     background_hops_dict['background_source'],
#                     'promoter_source': promoter_region.source,
#                     'background_total_hops':
#                     background_hops_dict['background_total_hops'],
#                     'experiment_total_hops':
#                     experiment_hops_dict['experiment_total_hops'],
#                     'background_hops':
#                     background_hops_dict['background_hops'],
#                     'experiment_hops':
#                     experiment_hops_dict['experiment_hops'],
#                     'callingcards_enrichment': enrichment(
#                         background_hops_dict['background_total_hops'],
#                         experiment_hops_dict['experiment_total_hops'],
#                         background_hops_dict['background_hops'],
#                         experiment_hops_dict['experiment_hops'],
#                         query_params_dict.get('pseudo_count', 0.2)),
#                     'poisson_pval': poisson_pval(
#                         background_hops_dict['background_total_hops'],
#                         experiment_hops_dict['experiment_total_hops'],
#                         background_hops_dict['background_hops'],
#                         experiment_hops_dict['experiment_hops'],
#                         query_params_dict.get('pseudo_count', 0.2)),
#                     'hypergeometric_pval': hypergeom_pval(
#                         background_hops_dict['background_total_hops'],
#                         experiment_hops_dict['experiment_total_hops'],
#                         background_hops_dict['background_hops'],
#                         experiment_hops_dict['experiment_hops']),
#             }

#             results[index] = output_dict
#             index = index + 1

#     logger.info('Time to process %s promoters: %s',
#                 len(promoter_queryset), time.time() - start_time)

#     result_df = pd.DataFrame.from_dict(results)

#     return result_df


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
