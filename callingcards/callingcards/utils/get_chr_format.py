from ..models.ChrMap import ChrMap


def get_chr_format(unique_chr_values_set: set) -> str:
    """
    Check if all unique values in df['chr'] are contained in at least one of
        the fields of the chr_map table.

    Args:
        unique_chr_values_set (set): a set of chromosome names

    Returns:
        str: The name of the first field in ChrMap for which all df['chr']
            values are found, or None if not found.

    Raises:
        ValueError: if the unique_chr_values_set is not a subset of any of the
        ChrMap Fields
    """
    chrmap_fields = [field.name for field in ChrMap._meta.get_fields()
                     if field.concrete and field.name not in
                     ['id', 'seqlength', 'type', 'uploader', 'uploadDate',
                      'modified', 'modifiedBy']]

    chr_map_records = ChrMap.objects.all()

    # Check each field in ChrMap
    for field in chrmap_fields:
        chr_map_values = set(getattr(record, field)
                             for record in chr_map_records)
        if unique_chr_values_set.issubset(chr_map_values):
            return field

    raise ValueError('chromosome naming convention not in ChrMap table. '
                     'Add a new field to ChrMap, or change the naming '
                     'convention to one that is already recognized')
