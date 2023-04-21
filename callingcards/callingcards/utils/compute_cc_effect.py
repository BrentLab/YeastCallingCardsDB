def compute_cc_effect(expression_hops,
                      total_expression_hops,
                      background_hops,
                      total_background_hops,
                      pseudocount=0.2):

    numerator = ((expression_hops / total_expression_hops) + pseudocount)
    denominator = ((background_hops / total_background_hops) + pseudocount)

    return (numerator / denominator)
