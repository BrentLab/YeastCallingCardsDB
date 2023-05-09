from typing import List, Tuple
import pandas as pd

from django.core.exceptions import FieldError

from callingcards.callingcards.models import ChrMap


def validate_chromosomes(
        df: pd.DataFrame, chr_format: str) -> bool:
    """Check that the unique values in the first column of the file correspond 
        to at least one of the fields of the ChrMap table.

    :param df: a pandas dataframe of the qBed/ccf file
    :type df: pd.DataFrame
    :param chr_format: the format of the chromosome names in the file
    :type chr_format: str
    :return: True if the chromosome names in the file match at least one of the
        fields in ChrMap
    :rtype: bool

    :raises ValueError: if chr_format is not a valid field in ChrMap
    :raises ValueError: if the chromosome names in the file do not match at
        least one of the fields in ChrMap
    """
    try:
        valid_chr_list = {x[0] for x
                          in ChrMap.objects.values_list(chr_format) if
                          x[0] not in {'uploader', 'uploadDate',
                                       'modified', 'modifiedBy',
                                       'seqlength'}}
    except FieldError as exc:
        raise ValueError(f'{chr_format} is not a valid field in ChrMap') \
            from exc

    df_chr_set = set(df.iloc[:, 0].unique())

    # check that the chromosome names in the file match at least one of the
    # fields in ChrMap
    invalid_chr_set = df_chr_set - valid_chr_list

    if invalid_chr_set:
        raise ValueError(f'The following chromosomes in the uploaded file '
                         f'do not match any chromosomes in the database '
                         f'for field {chr_format}: '
                         f'{invalid_chr_set}')
    else:
        return True


def validate_coordinates(df: pd.DataFrame,
                         chrmap_field: str) -> List[Tuple[str, int]]:

    if chrmap_field not in [field.name for field in ChrMap._meta.fields]:
        raise ValueError(f'{chrmap_field} is not a valid field in ChrMap')

    agg_func = {
        'start': 'min',   # minimum value of second column
        'end': 'max'    # maximum value of third column
    }

    grouped_df = df.groupby('chr', as_index=False).agg(agg_func)

    chrmap_queryset = ChrMap.objects.all()\
        .values(chrmap_field, 'seqlength')

    # Convert the QuerySet to a dictionary
    chrmap_dict = {row[chrmap_field]: row['seqlength']
                   for row in chrmap_queryset}

    invalid_coordinates = []
    for row in grouped_df.itertuples(index=False):
        try:
            chr_seqlength = chrmap_dict.get(row[0])
        except KeyError as err:
            raise (f'The chromosome name {row[0]} was not found in '
                   f'the {chrmap_field} field of ChrMap') from err
        if row[1] < 0:
            invalid_coordinates.append((row[0], row[1]))
        if row[2] > chr_seqlength+1:
            invalid_coordinates.append((row[0], row[2]))

    return invalid_coordinates


def validate_strand(df: pd.DataFrame) -> List[Tuple[str, str]]:

    strand_entries = df.loc[:, 'strand'].unique()
    invalid_strands = []
    for strand_level in strand_entries:
        if strand_level not in ['+', '-', '*']:
            invalid_strands.append(strand_level)

    return invalid_strands
