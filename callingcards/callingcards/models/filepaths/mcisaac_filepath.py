def mcisaac_filepath(instance, filename):
    tf = instance.tf
    strain = instance.strain
    date = instance.date
    time = instance.time
    restriction = instance.restriction
    mechanism = instance.mechanism
    return f'mcisaac/{tf.locus_tag}_{strain}_{date}_{time}_{restriction}_{mechanism}.csv.gz'