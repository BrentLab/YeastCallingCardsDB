import logging
import pandas as pd
from .check_chr_format import check_chr_format

logger = logging.getLogger('__name__')


def validate_bed6_df(df: pd.DataFrame, chr_format: str) -> bool:
    """
    Check if the DataFrame conforms to the BED6 format.

    Args:
        df (pd.DataFrame): The DataFrame to check
        chr_format (str): The name of a field in the ChrMap table for which all
            levels of the `chr` column are contained

    Returns:
        bool: True if the DataFrame conforms to the BED6 format

    Raises:
        ValueError: if the DataFrame does not conform to the BED6 format
    """
    required_columns = ['chr', 'start', 'end', 'name', 'score', 'strand']

    # Check if all required columns are present
    if not all(column in df.columns for column in required_columns):
        raise ValueError('This upload requires that the bed file have the '
                         'following column headers: %s'
                         '"' + '", " '.join(required_columns) + '"')
    # cast chr to a string
    df['chr'] = df['chr'].astype(str)
    df['name'] = df['name'].astype(str)
    # Note: this will raise a ValueError if the set of chr levels is not a
    # subset of one of the fields in ChrMap
    if not check_chr_format(set(df['chr'].unique()), chr_format):
        raise ValueError('the levels of the `chr` column are not a subset of '
                         'the levels of %s in the ChrMap table' % chr_format)

    if not pd.api.types.is_integer_dtype(df['start']):
        raise ValueError('`start` must be an integer valued column')

    if not pd.api.types.is_integer_dtype(df['end']):
        raise ValueError('`end` must be an integer valued column')
    if not pd.api.types.is_object_dtype(df['name']):
        raise ValueError('`name` must be a str column.')
    if not (pd.api.types.is_integer_dtype(df['score'])
            or pd.api.types.is_float_dtype(df['score'])):
        raise ValueError('`score` must be an integer or float column')
    if not set(df['strand']).issubset({'+', '-', '*'}):
        raise ValueError('`strand` must be one of `+`, `-` or `*`')

    # Check if 'start' is less than or equal to 'end'
    if any(df['start'] > df['end']):
        raise ValueError('`start` should always be before `end`. there exists '
                         'a row for which this is not true.')

    return True
