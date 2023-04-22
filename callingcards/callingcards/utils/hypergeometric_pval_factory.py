from typing import Callable
import logging
import pandas as pd
import scipy.stats as scistat

logger = logging.getLogger(__name__)


def hypergeometric_pval_factory(df: pd.DataFrame) -> Callable[[int, int], float]:
    """
    Create a Hypergeometric p-value calculator based on the given DataFrame.

    :param df: A DataFrame containing 'background_hops' and 'experiment_hops' columns.
    :type df: pd.DataFrame

    :return: A function that takes the background and experiment hops and
             calculates the Hypergeometric p-value.
    :rtype: Callable[[int, int], float]
    """
    total_bg_hops = df['background_hops'].sum()
    total_expr_hops = df['experiment_hops'].sum()
    M = total_bg_hops + total_expr_hops
    n = total_expr_hops

    def pval(bg_hops, expr_hops):
        """
        Calculate the Hypergeometric p-value for the given background and experiment hops.

        :param bg_hops: Background hops count.
        :type bg_hops: int
        :param expr_hops: Experiment hops count.
        :type expr_hops: int

        :return: Hypergeometric p-value.
        :rtype: float
        """
        x = expr_hops - 1
        N = bg_hops + expr_hops

        return 1 - scistat.hypergeom.cdf(x, M, n, N)

    return pval
