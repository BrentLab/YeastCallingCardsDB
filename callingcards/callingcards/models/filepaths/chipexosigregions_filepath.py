def chipexosigregions_filepath(instance, filename):
    instance_id = instance.id
    source = instance.promoterregions_source
    return f'chipexo/{source}/{instance_id}.tsv.gz'