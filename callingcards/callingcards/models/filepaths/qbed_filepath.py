def qbed_filepath(instance, filename):
    experiment = instance.experiment
    return f'qbed/{experiment.batch}/ccexperiment_{experiment.id}.qbed'