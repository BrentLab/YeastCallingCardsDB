def harbisonchip_filepath(instance, filename):
    instance_id = instance.id
    return f'harbison/{instance_id}.tsv.gz'