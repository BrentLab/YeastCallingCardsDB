def chipexosigregions_filepath(instance, filename):
    chipexo_id = instance.chipexo_id
    promoterregion_id = instance.promoterregions_id
    return f'chipexo/{chipexo_id}_{promoterregion_id}.tsv.gz'