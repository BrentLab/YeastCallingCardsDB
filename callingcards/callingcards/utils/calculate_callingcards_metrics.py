
import logging
import scipy.stats as scistat
import pandas as pd

logger = logging.getLogger(__name__)


def calculate_callingcards_metrics(row):

    for key in ['background_total_hops', 'experiment_total_hops',
                'background_hops', 'experiment_hops']:
        if key not in row:
            logger.error(row)
            raise ValueError(f'{key} not in row')

    total_background_hops = row['background_total_hops']
    total_experiment_hops = row['experiment_total_hops']
    background_hops = row['background_hops']
    experiment_hops = row['experiment_hops']

    effect = calling_cards_effect(
        total_background_hops, total_experiment_hops,
        background_hops, experiment_hops)

    poisson_pval_result = poison_pval(
        total_background_hops, total_experiment_hops,
        background_hops, experiment_hops)

    hypergeom_pval_result = hypergeom_pval(
        total_background_hops, total_experiment_hops,
        background_hops, experiment_hops)

    return pd.Series({'effect': effect,
                      'poisson_pval': poisson_pval_result,
                      'hypergeom_pval': hypergeom_pval_result})


def calling_cards_effect(total_background_hops: int,
                         total_experiment_hops: int,
                         background_hops: int,
                         experiment_hops: int,
                         pseudocount: float = 0.2):

    numerator = ((experiment_hops / total_experiment_hops) + pseudocount)
    denominator = ((background_hops / total_background_hops) + pseudocount)

    return (numerator / denominator)


def poison_pval(total_background_hops: int,
                total_experiment_hops: int,
                background_hops: int,
                experiment_hops: int,
                pseudocount: float = 0.2) -> float:
    """
    Calculate the Poisson p-value for the given background and experiment hops.

    :param bg_hops: Background hops count.
    :type bg_hops: int
    :param expr_hops: Experiment hops count.
    :type expr_hops: int

    :return: Poisson p-value.
    :rtype: float
    """
    hop_ratio = total_experiment_hops / total_background_hops
    mu = (background_hops * hop_ratio) + pseudocount
    x = experiment_hops + pseudocount

    return 1 - scistat.poisson.cdf(x, mu)


def hypergeom_pval(total_background_hops: int,
                   total_experiment_hops: int,
                   background_hops: int,
                   experiment_hops: int) -> float:
    """
    Calculate the Hypergeometric p-value for the given background 
    and experiment hops.

    :param bg_hops: Background hops count.
    :type bg_hops: int
    :param expr_hops: Experiment hops count.
    :type expr_hops: int

    :return: Hypergeometric p-value.
    :rtype: float
    """
    M = total_background_hops + total_experiment_hops
    n = total_experiment_hops

    x = experiment_hops - 1
    N = background_hops + experiment_hops

    return 1 - scistat.hypergeom.cdf(x, M, n, N)
