import os
import logging

logger = logging.getLogger(__name__)

def cc_replicate_sig_filepath(instance, filename):
    experiment = instance.experiment
    promoter_source = instance.promoter_source
    path = os.path.join(
        'analysis',
        experiment.batch,
        f'ccexperiment_{experiment.id}_{promoter_source.pk}.csv.gz')
    logger.debug("CallingCardsSig filepath: %s", path)
    return path