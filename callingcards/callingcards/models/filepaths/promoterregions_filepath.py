def promoterregions_filepath(instance, filename):
    instance_id = instance.id
    return f'promoter_regions/{instance_id}.tsv.gz'