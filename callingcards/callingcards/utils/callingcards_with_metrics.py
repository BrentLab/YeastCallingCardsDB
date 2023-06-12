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
import requests
import tempfile

from django.core.files.storage import default_storage
from django.db.models import Count
from django.db.utils import NotSupportedError
import scipy.stats as scistat
import pandas as pd

from ..models import (ChrMap, PromoterRegions, Background, Hops_s3)
from ..filters import PromoterRegionsFilter, Hops_s3Filter, BackgroundFilter

logger = logging.getLogger(__name__)


def callingcards_with_metrics(query_params_dict: dict) -> pd.DataFrame:
    # read experiment data into memory
    experiment_counts_df, filtered_experiment_df = \
        experiment_data(query_params_dict)

    # read promoter regions data into memory
    filtered_promoters_df = promoter_data(query_params_dict)

    # read background data into memory
    background_counts_df, filtered_background_df = \
        background_data(query_params_dict)

    # by default, False
    consider_strand = bool(query_params_dict.get('consider_strand', False))

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
        # Filter experiment and background hops based on
        # promoter and strand
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
        # note the renaming of background_source
        bg_hops_count = filtered_bg_hops[
            (filtered_bg_hops['chr_id'] == promoter_row['chr_id']) &
            (filtered_bg_hops['start'] >= promoter_row['start']) &
            (filtered_bg_hops['start'] <= promoter_row['end'])]\
            .groupby('source_id')\
            .agg({'background_total_hops': 'first', 'chr_id': 'count'})\
            .reset_index()\
            .rename(columns={'chr_id': 'background_hops'})

        # Perform an outer merge with background_counts_df
        bg_hops_count = background_counts_df\
            .merge(bg_hops_count, on='source_id', how='left')\
            .rename(columns={'source_id': 'background_source'})

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

        # Create a boolean mask for columns starting with
        # "background" or "experiment"
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

        merged_df['promoter_id'] = promoter_row['id']
        merged_df['promoter_source'] = promoter_row['source_id']
        merged_df['target_gene_id'] = promoter_row['associated_feature_id']

        return merged_df

    start_time = time.time()
    # Apply the process_promoter_row function to each row
    # in filtered_promoters_df
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


def translate_chr_to_id(df, chr_format):
    """Given a dataframe with the column `chr` and a chromosome format, 
    which is a field in the ChrMap model, use the ChrMap model to translate 
    the original `chr` field in the dataframe to the corresponding `chr_id`

    :param df: A dataframe representing a qbed format file
    :dtype df: pandas.DataFrame
    :param chr_format: A string representing the chromosome format
    :dtype chr_format: str

    :return: A dataframe with the `chr` field replaced by `chr_id`
    :rtype: pandas.DataFrame
    """
    # Get the corresponding ChrMap object
    chr_map_dict = dict(ChrMap.objects.values_list(chr_format, 'id'))

    # Replace the chr column with chr_id
    df['chr'] = df['chr'].map(chr_map_dict)

    return df


def experiment_data(query_params_dict):

    # filter the Hops (calling cards experiments) model objects
    filtered_experiment_queryset = Hops_s3Filter(
        query_params_dict,
        queryset=Hops_s3.objects.all())\
        .qs\
        .select_related('experiment')\
        .exclude(experiment__tf__tf__locus_tag='undetermined')

    try:
        # Attempt to use DISTINCT ON fields
        if len(filtered_experiment_queryset.distinct('experiment_id')) == 0:
            raise ValueError('No experiments found for {}. No action taken.'
                             .format(query_params_dict))
    except NotSupportedError as exc:
        # Alternate method if DISTINCT ON fields is not supported
        experiment_ids = filtered_experiment_queryset.values_list(
            'experiment_id', flat=True)
        unique_experiment_ids = set(experiment_ids)

        if len(unique_experiment_ids) == 0:
            raise ValueError(f'No experiments found for {query_params_dict}. '
                             f'No action taken.') from exc

    dataframes = []
    experiment_counts_dict = {}

    for record in filtered_experiment_queryset:
        # Get the experiment_id
        experiment_id = record.experiment_id

        # get the experiment data
        # TODO write this as a function -- note the diff btwn .path and .url
        # .path works when the storage is a filesystem. .url is necessary
        # when the storage is s3
        try:
            file_location = record.qbed.path
        except NotImplementedError:
            file_location = record.qbed.url

        if file_location.startswith('http'):
            response = requests.get(file_location)

            with tempfile.NamedTemporaryFile() as temp_file:
                temp_file.write(response.content)
                temp_file.flush()
                df = pd.read_csv(temp_file.name, sep='\t')
        else:
            df = pd.read_csv(file_location, sep='\t')

        if record.chr_format != 'id':
            df = translate_chr_to_id(df, record.chr_format)

        df.rename(columns={'chr': 'chr_id'}, inplace=True)
        df['experiment_id'] = experiment_id

        # Add the DataFrame to the list of DataFrames
        dataframes.append(df)

        # add experiment counts, etc record
        experiment_counts_dict[experiment_id] = {
            'experiment_total_hops': df.shape[0],
            'tf_id': record.experiment.tf.tf_id,
            'experiment_batch': record.experiment.batch,
            'experiment_replicate': record.experiment.batch_replicate
        }

    # Convert experiment_counts_dict to a DataFrame
    filtered_experiment_df = pd.concat(dataframes, ignore_index=True)

    # Convert experiment_counts_dict to a DataFrame
    experiment_counts_df = pd.DataFrame(
        experiment_counts_dict.values(),
        index=experiment_counts_dict.keys())
    experiment_counts_df.index.name = 'experiment_id'

    # Prepare filtered_experiment_df for merging with the background data
    filtered_experiment_df = filtered_experiment_df.merge(
        experiment_counts_df, on='experiment_id', how='left')

    return experiment_counts_df, filtered_experiment_df


def promoter_data(query_params_dict):
    filtered_promoters = PromoterRegionsFilter(
        query_params_dict,
        queryset=PromoterRegions.objects.all())
    # read the promoter data into memory
    filtered_promoters_df = pd.DataFrame.from_records(
        filtered_promoters.qs.values())

    return filtered_promoters_df


def background_data(query_params_dict):

    # filter the Background model objects
    filtered_background = BackgroundFilter(
        query_params_dict,
        queryset=Background.objects.all())

    # Group by the experiment_id
    # count the number of records per group
    # and remove the default ordering, if any
    unique_background_counts = (
        filtered_background.qs
        .values('source_id')
        .annotate(record_count=Count('id'))
        .order_by())
    # Convert the result to a dictionary with experiment_id
    # as key and record_count as value
    background_counts_dict = {entry['source_id']:
                              {'background_total_hops':
                                  entry['record_count']}
                              for entry in unique_background_counts}

    # Convert background hops data to a DataFrame
    filtered_background_df = pd.DataFrame\
        .from_records(filtered_background.qs.values())

    # Create a DataFrame with background_counts_dict
    background_counts_df = pd.DataFrame(
        background_counts_dict.values(),
        index=background_counts_dict.keys())
    background_counts_df.index.name = 'source_id'

    # Prepare for merging with the experiment data
    filtered_background_df = filtered_background_df.merge(
        background_counts_df, on='source_id', how='left')

    return background_counts_df, filtered_background_df


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
