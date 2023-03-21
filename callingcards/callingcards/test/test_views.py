import logging
import json
import pytest

from django.forms.models import model_to_dict
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
import factory

from callingcards.users.models import User
from callingcards.users.test.factories import UserFactory
from callingcards.callingcards.models import ChrMap, Gene, PromoterRegions, \
    HarbisonChIP, KemmerenTFKO, McIsaacZEV, Background, CCTF, \
    CCExperiment, Hops, HopsReplicateSig, QcMetrics, QcManualReview, \
    QcR1ToR2Tf, QcR2ToR1Tf, QcTfToTransposon
from .factories import ChrMapFactory, GeneFactory, PromoterRegionsFactory, \
    HarbisonChIPFactory, KemmerenTFKOFactory, McIsaacZEVFactory, \
    BackgroundFactory, CCTFFactory, CCExperimentFactory, HopsFactory, \
    HopsReplicateSigFactory, QcMetricsFactory, QcManualReviewFactory, \
    QcR1ToR2TfFactory, QcR2ToR1TfFactory, QcTfToTransposonFactory

fake = Faker()


class TestChrMapViewSet(APITestCase):
    """
    Tests /chrmap detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.chr_data = factory.build(dict, FACTORY_CLASS=ChrMapFactory)
        tmp, self.uploadDate, self.modified = \
            [self.chr_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('chrmap-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.chr_data)
        assert response.status_code == status.HTTP_201_CREATED

        chr = ChrMap.objects.get(pk=response.data.get('id'))
        assert chr.chr == self.chr_data.get('chr')
        assert chr.uploader.username == self.user.username


class TestGeneViewSet(APITestCase):
    """
    Tests /gene detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.gene_data = factory.build(dict, FACTORY_CLASS=GeneFactory)
        self.gene_data['chr'] = self.chr_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.gene_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('gene-list')
        settings.DEBUG = True
        self.gene_record_bulk_data = factory.build_batch(
            dict, 
            10, 
            FACTORY_CLASS=GeneFactory)
        for rec in self.gene_record_bulk_data:
            rec['chr'] = self.chr_record.pk
            tmp = [rec.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.gene_data)
        assert response.status_code == status.HTTP_201_CREATED

        gene = Gene.objects.get(pk=response.data.get('id'))
        assert gene.locus_tag == self.gene_data.get('locus_tag')
        assert gene.uploader.username == self.user.username

    def test_put_bulk(self):
        response = self.client.post(self.url, 
                                    data=json.dumps(self.gene_record_bulk_data),
                                    content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED


class TestPromoterRegionsViewSet(APITestCase):
    """
    Tests /promoter_regions detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.promoter_regions_data = factory.build(dict, FACTORY_CLASS=PromoterRegionsFactory)
        self.promoter_regions_data['chr'] = self.chr_record.pk
        self.promoter_regions_data['associated_feature'] = self.gene_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.promoter_regions_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('promoterregions-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.promoter_regions_data)
        assert response.status_code == status.HTTP_201_CREATED

        promoter_regions = PromoterRegions.objects.get(pk=response.data.get('id'))
        assert promoter_regions.associated_feature.pk == self.promoter_regions_data.get('associated_feature')
        assert promoter_regions.uploader.username == self.user.username


class TestHarbisonChIP(APITestCase):
    """
    Tests /harbison_chip detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.harbison_chip_data = factory.build(dict, FACTORY_CLASS=HarbisonChIPFactory)
        self.harbison_chip_data['gene'] = self.gene_record.pk
        self.harbison_chip_data['tf'] = self.gene_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.harbison_chip_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('harbisonchip-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.harbison_chip_data)
        assert response.status_code == status.HTTP_201_CREATED

        harbison_chip = HarbisonChIP.objects.get(pk=response.data.get('id'))
        assert harbison_chip.tf.pk == self.harbison_chip_data.get('tf')
        assert harbison_chip.uploader.username == self.user.username


class TestKemmerenTFKO(APITestCase):
    """
    Tests /kemmeren_tfko detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.kemmeren_tfko_data = factory.build(dict, FACTORY_CLASS=KemmerenTFKOFactory)
        self.kemmeren_tfko_data['gene'] = self.gene_record.pk
        self.kemmeren_tfko_data['tf'] = self.gene_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.kemmeren_tfko_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('kemmerentfko-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.kemmeren_tfko_data)
        assert response.status_code == status.HTTP_201_CREATED

        kemmeren_tfko = KemmerenTFKO.objects.get(pk=response.data.get('id'))
        assert kemmeren_tfko.tf.pk == self.kemmeren_tfko_data.get('tf')
        assert kemmeren_tfko.uploader.username == self.user.username


class TestMcIsaacZEV(APITestCase):
    """
    Tests /mcisaac_zev detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.mcisaac_zev_data = factory.build(dict, FACTORY_CLASS=McIsaacZEVFactory)
        self.mcisaac_zev_data['gene'] = self.gene_record.pk
        self.mcisaac_zev_data['tf'] = self.gene_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.mcisaac_zev_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('mcisaaczev-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.mcisaac_zev_data)
        assert response.status_code == status.HTTP_201_CREATED

        mcisaac_zev = McIsaacZEV.objects.get(pk=response.data.get('id'))
        assert mcisaac_zev.tf.pk == self.mcisaac_zev_data.get('tf')
        assert mcisaac_zev.uploader.username == self.user.username


class TestBackground(APITestCase):
    """
    Tests /background detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.background_data = factory.build(dict, FACTORY_CLASS=BackgroundFactory)
        self.background_data['chr'] = self.chr_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.background_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('background-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.background_data)
        assert response.status_code == status.HTTP_201_CREATED

        background = Background.objects.get(pk=response.data.get('id'))
        assert background.chr.pk == self.background_data.get('chr')
        assert background.uploader.username == self.user.username

class TestCCTF(APITestCase):
    """
    Tests /cctf detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.cctf_data = factory.build(dict, FACTORY_CLASS=CCTFFactory)
        self.cctf_data['tf'] = self.gene_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.cctf_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('cctf-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.cctf_data)
        assert response.status_code == status.HTTP_201_CREATED

        cctf = CCTF.objects.get(pk=response.data.get('id'))
        assert cctf.tf.pk == self.cctf_data.get('tf')
        assert cctf.uploader.username == self.user.username


class TestCCExperiment(APITestCase):
    """
    Tests /ccexperiment detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.cctf_record = CCTFFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.ccexperiment_data = factory.build(dict, FACTORY_CLASS=CCExperimentFactory)
        self.ccexperiment_data['tf'] = self.cctf_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.ccexperiment_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('ccexperiment-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.ccexperiment_data)
        assert response.status_code == status.HTTP_201_CREATED

        ccexperiment = CCExperiment.objects.get(pk=response.data.get('id'))
        assert ccexperiment.tf.pk == self.ccexperiment_data.get('tf')
        assert ccexperiment.uploader.username == self.user.username


class TestHops(APITestCase):
    """
    Tests /hops detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.hops_data = factory.build(dict, FACTORY_CLASS=HopsFactory)
        self.hops_data['chr'] = self.chr_record.pk
        self.hops_data['experiment'] = self.experiment_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.hops_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('hops-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.hops_data)
        assert response.status_code == status.HTTP_201_CREATED

        hops = Hops.objects.get(pk=response.data.get('id'))
        assert hops.chr.pk == self.hops_data.get('chr')
        assert hops.experiment.pk == self.hops_data.get('experiment')
        assert hops.uploader.username == self.user.username

class TestHopsReplicateSig(APITestCase):
    """
    Tests /hopsreplicatesig detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.hopsreplicatesig_data = factory.build(dict, FACTORY_CLASS=HopsReplicateSigFactory)
        self.hopsreplicatesig_data['experiment'] = self.experiment_record.pk
        self.hopsreplicatesig_data['chr'] = self.chr_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.hopsreplicatesig_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('hopsreplicatesig-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.hopsreplicatesig_data)
        assert response.status_code == status.HTTP_201_CREATED

        hopsreplicatesig = HopsReplicateSig.objects.get(pk=response.data.get('id'))
        assert hopsreplicatesig.chr.pk == self.hopsreplicatesig_data.get('chr')
        assert hopsreplicatesig.experiment.pk == self.hopsreplicatesig_data.get('experiment')
        assert hopsreplicatesig.uploader.username == self.user.username


class TestQcMetrics(APITestCase):
    """
    Tests /qcmetrics detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qcmetrics_data = factory.build(dict, FACTORY_CLASS=QcMetricsFactory)
        self.qcmetrics_data['experiment'] = self.experiment_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.qcmetrics_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('qcmetrics-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qcmetrics_data)
        assert response.status_code == status.HTTP_201_CREATED

        qcmetrics = QcMetrics.objects.get(pk=response.data.get('id'))
        assert qcmetrics.experiment.pk == self.qcmetrics_data.get('experiment')
        assert qcmetrics.uploader.username == self.user.username


class TestQcR1ToR2Tf(APITestCase):
    """
    Tests /qcr1tor2tf detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qcr1tor2tf_data = factory.build(dict, FACTORY_CLASS=QcR1ToR2TfFactory)
        self.qcr1tor2tf_data['experiment'] = self.experiment_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.qcr1tor2tf_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('qcr1tor2tf-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qcr1tor2tf_data)
        assert response.status_code == status.HTTP_201_CREATED

        qcr1tor2tf = QcR1ToR2Tf.objects.get(pk=response.data.get('id'))
        assert qcr1tor2tf.experiment.pk == self.qcr1tor2tf_data.get('experiment')
        assert qcr1tor2tf.uploader.username == self.user.username

class TestQcR2ToR1Tf(APITestCase):
    """
    Tests /qcr2tor1tf detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qcr2tor1tf_data = factory.build(dict, FACTORY_CLASS=QcR2ToR1TfFactory)
        self.qcr2tor1tf_data['experiment'] = self.experiment_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.qcr2tor1tf_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('qcr2tor1tf-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qcr2tor1tf_data)
        assert response.status_code == status.HTTP_201_CREATED

        qcr2tor1tf = QcR2ToR1Tf.objects.get(pk=response.data.get('id'))
        assert qcr2tor1tf.experiment.pk == self.qcr2tor1tf_data.get('experiment')
        assert qcr2tor1tf.uploader.username == self.user.username

class TestQcTfToTransposon(APITestCase):
    """
    Tests /qctftotransposon detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qctftotransposon_data = factory.build(dict, FACTORY_CLASS=QcTfToTransposonFactory)
        self.qctftotransposon_data['experiment'] = self.experiment_record.pk
        tmp, self.uploadDate, self.modified = \
            [self.qctftotransposon_data.pop(x) for x in
             ['uploader', 'uploadDate', 'modified']]
        self.url = reverse('qctftotransposon-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def ttest_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qctftotransposon_data)
        assert response.status_code == status.HTTP_201_CREATED

        qctftotransposon = QcTfToTransposon.objects.get(pk=response.data.get('id'))
        assert qctftotransposon.experiment.pk == self.qctftotransposon_data.get('experiment')
        assert qctftotransposon.uploader.username == self.user.username
