def promoterregions_filepath(instance, filename):
    promoter_regions_source = instance.source
    return f'promoter_regions/{promoter_regions_source}.tsv.gz'