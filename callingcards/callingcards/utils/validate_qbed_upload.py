from typing import List, Tuple
import pandas as pd
from callingcards.callingcards.models import ChrMap

def validate_chromosomes(df: pd.DataFrame) -> Tuple[str, List[str]]:
    """Check that the unique values in the first column of the file correspond 
        to at least one of the fields of the ChrMap table.

    :param df: a pandas dataframe of the qBed/ccf file
    :type df: pd.DataFrame
    :return: if successful, returns a tuple containing the name of the 
        matching field in ChrMap and an empty list; otherwise, returns a 
        tuple containing the most similar field in ChrMap and a list of 
        invalid chromosome names.
    :rtype: Tuple[str, List[str]]
    """
    field_names = [f.name for f in ChrMap._meta.get_fields()
                   if f.name not in ['background',
                                     'gene',
                                     'hops',
                                     'promoterregions',
                                     'uploader',
                                     'uploadDate',
                                     'modified',
                                     'modifiedBy',
                                     'seqlength']]

    chr_maps = ChrMap.objects.values_list(*field_names)

    # create a dictionary to map each chromosome name to a field in ChrMap
    chr_name_to_field = {}
    for chr_map in chr_maps:
        for i, name in enumerate(chr_map):
            chr_name_to_field[name] = field_names[i]

    invalid_chromosomes = []
    matched_field = None

    chrom_names = df.iloc[:, 0].unique()
    for name in chrom_names:
        if name in chr_name_to_field:
            if matched_field is None:
                matched_field = chr_name_to_field[name]
        else:
            invalid_chromosomes.append(name)

    if matched_field is None:
        # if no match is found, find the most similar field in ChrMap
        most_similar_field = None
        max_matching_chars = 0
        for field in field_names:
            matching_chars = 0
            for chr_map in chr_maps:
                if chr_map[field_names.index(field)] in chrom_names:
                    matching_chars += 1
            if matching_chars > max_matching_chars:
                max_matching_chars = matching_chars
                most_similar_field = field

        return (most_similar_field, invalid_chromosomes)
    else:
        return (matched_field, invalid_chromosomes)


def validate_coordinates(df: pd.DataFrame, 
                         chrmap_field: str) -> List[Tuple[str, int]]:

    if chrmap_field not in [field.name for field in ChrMap._meta.fields]:
        raise ValueError(f'{chrmap_field} is not a valid field in ChrMap')
        
    agg_func = {
        1: 'min',   # minimum value of second column
        2: 'max'    # maximum value of third column
    }

    grouped_df = df.groupby(0, as_index=False).agg(agg_func)

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

    strand_entries = df.iloc[:, 4].unique()
    invalid_strands = []
    for strand_level in strand_entries:
        if strand_level not in ['+', '-', '*']:
            invalid_strands.append(strand_level)
    
    return invalid_strands