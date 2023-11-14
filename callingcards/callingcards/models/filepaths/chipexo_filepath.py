def chipexo_filepath(instance, filename):
    chipexo_id = instance.chipexo_id
    return f'chipexo/{chipexo_id}.tsv.gz'