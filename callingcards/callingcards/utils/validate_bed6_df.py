import logging
import pandas as pd
from .get_chr_format import get_chr_format

logger = logging.getLogger('__name__')


def validate_bed6_df(df: pd.DataFrame) -> str:
    """
    Check if the DataFrame conforms to the BED6 format.

    Args:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        str: The first field in the ChrMap table for which all levels of the
            `chr` column are contained
    
    Raises:
        ValueError: if any of the expectations on the bed6 dataframe are not
            met  
    """
    required_columns = ['chr', 'start', 'end', 'name', 'score', 'strand']

    # Check if all required columns are present
    if not all(column in df.columns for column in required_columns):
        raise ValueError('This upload requires that the bed file have the '
                         'following column headers: %s' 
                         '"' + '", " '.join(required_columns) + '"')
    # cast chr to a string
    df['chr'] = df['chr'].astype(str)
    # Note: this will raise a ValueError if the set of chr levels is not a 
    # subset of one of the fields in ChrMap
    chr_format = get_chr_format(set(df['chr'].unique()))
     
    if not pd.api.types.is_integer_dtype(df['start']):
        validation_flag = False
    
    if not pd.api.types.is_integer_dtype(df['end']):
        raise ValueError('`end` must be an integer valued column')
    if not pd.api.types.is_object_dtype(df['name']):
        raise ValueError('`Name` must be a str column. If this is numeric, '
                         'consider adding a string as a prefix to the number.')
    if not (pd.api.types.is_integer_dtype(df['score'])
            or pd.api.types.is_float_dtype(df['score'])):
        raise ValueError('`score` must be an integer or float column')
    if not set(df['strand']).issubset({'+', '-', '*'}):
        raise ValueError('`strand` must be one of `+`, `-` or `*`')

    # Check if 'start' is less than or equal to 'end'
    if any(df['start'] > df['end']):
        raise ValueError('`start` should always be before `end`. there exists '
                         'a row for which this is not true.')

    return chr_format
