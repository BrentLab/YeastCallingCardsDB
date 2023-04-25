import pytest
# import pandas as pd
# import pandas.testing as pdt
from rest_framework.test import APITestCase
from .factories import PromoterRegionsFactory, HopsFactory, BackgroundFactory
from ..utils.callingcards_with_metrics import (enrichment,
                                               poisson_pval,
                                               hypergeom_pval,
                                               callingcards_with_metrics)

class TestCallingCardsWithMetrics(APITestCase):

    def setUp(self):
        # Create a test dataset using factories
        self.promoter_regions = PromoterRegionsFactory.create_batch(10)
        self.hops = HopsFactory.create_batch(10)
        self.backgrounds = BackgroundFactory.create_batch(10)

    def test_callingcards_with_metrics(self):
        # query_params_dict = {
        #     'promoter_source': 'yiming',
        #     'experiment_id': 75,
        #     'background_source': 'adh1',
        #     'consider_strand': False
        # }

        query_params_dict_1 = {}

        # Call the function with the test dataset
        actual_1 = callingcards_with_metrics(query_params_dict_1)

        assert len(actual_1) == 100

        query_params_dict_2 = {
            'consider_strand': True
        }

        actual_2 = callingcards_with_metrics(query_params_dict_2)

        assert 2 == 2

        # Expected result DataFrame
        # Replace with the expected values based on your test dataset
        # expected = pd.DataFrame({
        #     'promoter_id': [...],
        #     'experiment_id': [...],
        #     'background_source': [...],
        #     'promoter_source': [...],
        #     'background_hops': [...],
        #     'background_total_hops': [...],
        #     'experiment_hops': [...],
        #     'experiment_total_hops': [...],
        #     'callingcards_enrichment': [...],
        #     'poisson_pval': [...],
        #     'hypergeometric_pval': [...]
        # })
        # Compare the resulting DataFrame with the expected result
        # pdt.assert_frame_equal(actual, expected, check_dtype=False)

def test_enrichment():
    test_1 = {
        'total_background_hops': 10,
        'total_experiment_hops': 10,
        'background_hops': 5,
        'experiment_hops': 5,
        'pseudocount': 1e-10
    }

    actual_1 = enrichment(**test_1)
    expected_1 = 1
    assert actual_1 == pytest.approx(expected_1,
                                     rel=1e-9)

    test_2 = {
        'total_background_hops': 0,
        'total_experiment_hops': 0,
        'background_hops': 0,
        'experiment_hops': 0,
        'pseudocount': 0.2
    }

    assert_2 = enrichment(**test_2)
    expected_2 = 0
    assert assert_2 == expected_2

    test_3 = {
        'total_background_hops': 0,
        'total_experiment_hops': 0,
        'background_hops': 5,
        'experiment_hops': 5,
        'pseudocount': 1e-10
    }

    actual_3 = enrichment(**test_3)
    expected_3 = 1
    assert actual_3 == pytest.approx(expected_3,
                                     rel=1e-9)

def test_poisson_pval():
    test_1 = {
        'total_background_hops': 10,
        'total_experiment_hops': 10,
        'background_hops': 5,
        'experiment_hops': 5,
        'pseudocount': 1e-10
    }

    actual_1 = poisson_pval(**test_1)
    expected_1 = 0.38404
    assert actual_1 == pytest.approx(expected_1,
                                     rel=1e-4)

    test_2 = {
        'total_background_hops': 0,
        'total_experiment_hops': 10,
        'background_hops': 10,
        'experiment_hops': 10,
        'pseudocount': 1e-10
    }

    actual_2 = poisson_pval(**test_2)
    expected_2 = 1
    assert actual_2 == pytest.approx(expected_2,
                                     rel=1e-4)

def test_hypergeom_pval():
    test_1 = {
        'total_background_hops': 10,
        'total_experiment_hops': 10,
        'background_hops': 5,
        'experiment_hops': 5
    }

    actual_1 = hypergeom_pval(**test_1)
    expected_1 = 0.67186
    assert actual_1 == pytest.approx(expected_1,
                                     rel=1e-4)

    test_2 = {
        'total_background_hops': 10,
        'total_experiment_hops': 10,
        'background_hops': 5,
        'experiment_hops': 0
    }

    actual_2 = hypergeom_pval(**test_2)
    expected_2 = 0.983746
    assert actual_2 == pytest.approx(expected_2,
                                     rel=1e-4)