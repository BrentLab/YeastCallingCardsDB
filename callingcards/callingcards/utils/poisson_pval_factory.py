from typing import Callable
import logging
import pandas as pd
import scipy.stats as scistat

logger = logging.getLogger(__name__)

def poisson_pval_factory(df: pd.DataFrame, pseudocount: float) -> Callable[[int, int], float]:
    """
    Create a Poisson p-value calculator based on the given DataFrame.

    :param df: A DataFrame containing 'background_hops' and 'experiment_hops' columns.
    :type df: pd.DataFrame
    :param pseudocount: A small constant added to avoid division by zero.
    :type pseudocount: float

    :return: A function that takes the background and experiment hops and
             calculates the Poisson p-value.
    :rtype: Callable[[int, int], float]
    """
    total_bg_hops = df['background_hops'].sum()
    total_expr_hops = df['experiment_hops'].sum()
    hop_ratio = total_expr_hops / total_bg_hops

    def pval(bg_hops, expr_hops):
        """
        Calculate the Poisson p-value for the given background and experiment hops.

        :param bg_hops: Background hops count.
        :type bg_hops: int
        :param expr_hops: Experiment hops count.
        :type expr_hops: int

        :return: Poisson p-value.
        :rtype: float
        """
        mu = (bg_hops * hop_ratio) + pseudocount
        x = expr_hops + pseudocount

        return 1 - scistat.poisson.cdf(x, mu)

    return pval