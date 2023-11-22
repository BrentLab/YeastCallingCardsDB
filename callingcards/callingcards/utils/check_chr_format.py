from ..models.ChrMap import ChrMap


def check_chr_format(chr_values_set: set, chr_map_field: str) -> bool:
    """
    Check if all unique values in df['chr'] are contained in at least one of
        the fields of the chr_map table.

    Args:
        chr_values_set (set): a set of chromosome names
        chr_map_field (str): the name of a field in the ChrMap table

    Returns:
        bool: True if the chr_values_set is a subset of the chr_map_field,
            False otherwise

    Raises:
        ValueError: if the chr_map_field is not a field in the ChrMap table
    """
    chrmap_fields = [field.name for field in ChrMap._meta.get_fields()
                     if field.concrete and field.name not in
                     ['id', 'seqlength', 'type', 'uploader', 'uploadDate',
                      'modified', 'modifiedBy']]

    if chr_map_field not in chrmap_fields:
        raise ValueError('chr_map_field must be one of %s' % chrmap_fields)

    chr_map_records = ChrMap.objects.all()

    chr_map_values = set(getattr(record, chr_map_field)
                         for record in chr_map_records)

    return True if chr_values_set.issubset(chr_map_values) else False
