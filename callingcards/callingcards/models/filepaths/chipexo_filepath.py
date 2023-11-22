def chipexo_filepath(instance, filename):
    instance_id = instance.chipexo_id
    return f'chipexo/{instance_id}.tsv.gz'