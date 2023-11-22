def kemmerentfko_filepath(instance, filename):
    instance_id = instance.id
    return f'kemmeren/{instance_id}.tsv.gz'