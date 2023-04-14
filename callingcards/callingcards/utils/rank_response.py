import pandas as pd
import numpy as np
from typing import Callable


def get_common_columns(cc_df_subset):
    """
    Get the common column values from a subset of the cc_df_fltr DataFrame.

    Args:
        cc_df_subset (pd.DataFrame): A subset of the cc_df_fltr DataFrame 
        filtered by experiment.

    Returns:
        dict: A dictionary containing the common column values.
    """
    return {
        'tf_id': cc_df_subset['tf_id'].unique()[0],
        'tf_gene': cc_df_subset['tf_gene'].unique()[0],
        'tf_locus_tag': cc_df_subset['tf_locus_tag'].unique()[0],
        'experiment': cc_df_subset['experiment'].unique()[0],
        'background': cc_df_subset['background'].unique()[0],
        'promoter_source': cc_df_subset['promoter_source'].unique()[0],
        'bg_hops': 0,
        'expr_hops': 0,
        'poisson_pval': 1,
        'hypergeom_pval': 1
    }

def combine_columns(row, col_x, col_y):
    """
    Combine two columns by taking the non-null value from one of the columns.

    Args:
        row (pd.Series): A row from a DataFrame.
        col_x (str): The name of the first column to combine.
        col_y (str): The name of the second column to combine.

    Returns:
        The non-null value from either col_x or col_y.
    """
    return row[col_x] if pd.notna(row[col_x]) else row[col_y]

def combine_columns_np(df, col_x, col_y, new_col_name):
    """
    Combine two columns in a DataFrame by taking the non-null value from one of the columns.

    Args:
        df (pd.DataFrame): The DataFrame containing the columns to combine.
        col_x (str): The name of the first column to combine.
        col_y (str): The name of the second column to combine.
        new_col_name (str): The name of the new column with combined values.

    Returns:
        pd.DataFrame: A DataFrame with the new combined column.
    """
    mask = pd.isnull(df[[col_x, col_y]]).values
    df[new_col_name] = df[[col_x, col_y]].values[np.arange(len(df)), np.argmin(mask, axis=1)]
    return df

def process_cc_experiments(cc_df, promoter_df, experiment_map, binding_df,
                           expr_df) -> Callable[[str], pd.DataFrame]:
    """
    Create a function to process experiments with the given DataFrames.

    Args:
        cc_df (pd.DataFrame): The cc_df_fltr DataFrame.
        promoter_df (pd.DataFrame): The promoter_df DataFrame.
        experiment_map (pd.DataFrame): The experiment_map DataFrame.
        binding_df (pd.DataFrame): The binding_df_fltr DataFrame.
        expr_df (pd.DataFrame): The expr_df_fltr DataFrame.

    Returns:
        Callable[[str], pd.DataFrame]: A function that takes an experiment 
        number as input and returns a combined DataFrame.
    """
    def inner(experiment):
        # Filter cc_df by the given experiment and remove duplicate
        # promoter_ids
        cc_df_subset = cc_df[cc_df['experiment'] == experiment]\
            .drop_duplicates(subset='promoter_id')

        # Get the common columns in cc_df_subset
        col_list = get_common_columns(cc_df_subset)

        # Merge promoter_df and cc_df_subset on promoter_id
        result = promoter_df.merge(cc_df_subset, on='promoter_id', how='left')

        result = combine_columns_np(result, 'target_gene_id_x', 'target_gene_id_y', 'target_gene_id')
        result = combine_columns_np(result, 'target_locus_tag_x', 'target_locus_tag_y', 'target_locus_tag')
        result = combine_columns_np(result, 'target_gene_x', 'target_gene_y', 'target_gene')

        # Define the columns to be dropped
        columns_to_drop = ['target_gene_id_x', 'target_gene_id_y',
                           'target_locus_tag_x', 'target_locus_tag_y',
                           'target_gene_x', 'target_gene_y',
                           'experiment_batch', 'experiment_batch_replicate']

        # Drop the unnecessary columns
        result = result.drop(columns=columns_to_drop)
        join_col_list = ['tf_id', 'tf_locus_tag', 'tf_gene',
                         'target_gene_id', 'target_locus_tag',
                         'target_gene']
        # Fill NaN values in result using col_list, and merge with
        # experiment_map, binding_df, and expr_df
        result = result.fillna(col_list)\
            .merge(experiment_map, on='experiment', how='left')\
            .merge(binding_df, on=join_col_list, how='left')\
            .merge(expr_df, on=join_col_list, how='left')

        return result
    # return the inner function -- this may be called now on each experiment
    # in some TF set
    return inner
