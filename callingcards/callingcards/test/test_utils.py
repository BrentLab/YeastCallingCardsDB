import pytest
# import pandas as pd
# import pandas.testing as pdt
import os
from django.core.files.storage import default_storage
from django.urls import reverse
from rest_framework.test import APITestCase
from .factories import (PromoterRegionsFactory,
                        LabFactory,
                        CCExperimentFactory,
                        HopsSourceFactory,
                        Hops_s3Factory,
                        BackgroundFactory,
                        BackgroundSourceFactory,
                        PromoterRegionsSourceFactory,
                        GeneFactory)

from callingcards.users.test.factories import UserFactory

from ..utils.callingcards_with_metrics import (enrichment,
                                               poisson_pval,
                                               hypergeom_pval,
                                               callingcards_with_metrics)


class TestCallingCardsWithMetrics(APITestCase):
    def setUp(self):
        # Create a test dataset using factories
        self.user = UserFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.source_record = HopsSourceFactory.create()
        promoter_source = PromoterRegionsSourceFactory.create()
        self.promoter_regions = PromoterRegionsFactory.create_batch(
            10,
            source=promoter_source)
        background_source = BackgroundSourceFactory.create()
        self.lab_record = LabFactory.create()
        # self.hops = HopsFactory.create_batch(10)
        for i in range(10):
            ccexperiment = CCExperimentFactory.create(
                lab=self.lab_record)
            Hops_s3Factory.create(experiment=ccexperiment)

        self.backgrounds = BackgroundFactory.create_batch(
            10,
            source=background_source)
        self.gene_record = GeneFactory.create(gene='INO2')

    def test_callingcards_with_metrics(self):
        media_directory = default_storage.location
        qbed_file = 'qbed/run_6437/INO2_chrI.ccf'

        upload_file = os.path.join(media_directory, qbed_file)

        with open(upload_file, 'rb') as f:
            post_data = {
                'chr_format': 'ucsc',
                'tf_gene': 'INO2',
                'batch': 'run_6437',
                'batch_replicate': 1,
                'lab': self.lab_record.pk,
                'source': self.source_record.pk,
                'qbed': f,
                'notes': 'some notes'
            }

            # Test the create() method
            response = self.client.post(reverse('hopss3-list'),
                                        post_data,
                                        format='multipart')

        query_params = {
            'experiment_id': response.json()['experiment'],
            'hops_source': self.source_record.pk,
            'background_source': 'adh1',
            'promoter_source': 'yiming'
        }

        actual = callingcards_with_metrics(query_params)

        assert set(actual.columns) == {'experiment_id', 'tf_id',
                                       'experiment_batch',
                                       'experiment_replicate',
                                       'hops_source', 'experiment_hops',
                                       'experiment_total_hops',
                                       'background_source', 'background_hops',
                                       'background_total_hops',
                                       'callingcards_enrichment',
                                       'poisson_pval', 'hypergeometric_pval',
                                       'promoter_id',
                                       'promoter_source', 'target_gene_id'}

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
