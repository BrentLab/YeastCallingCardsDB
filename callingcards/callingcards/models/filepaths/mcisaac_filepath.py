def mcisaac_filepath(instance, filename):
    strain = instance.strain
    date = instance.date
    time = instance.time
    restriction = instance.restriction
    mechanism = instance.mechanism
    return f'mcisaac/{strain}_{date}_{time}_{restriction}_{mechanism}.csv.gz'