def hu_filepath(instance, filename):
    instance_id = instance.id
    return f'hu/{instance_id}.tsv.gz'