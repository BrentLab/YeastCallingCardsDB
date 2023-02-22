import logging
import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
import factory

from callingcards.users.models import User
from callingcards.users.test.factories import UserFactory
from callingcards.callingcards.models import ChrMap, Gene, PromoterRegions, \
    HarbisonChIP, KemmerenTFKO, Background, CCTF, CCExperiment, Hops, \
    HopsReplicateSig, QcMetrics, QcManualReview, QcR1ToR2Tf, QcR2ToR1Tf, \
    QcTfToTransposon
from .factories import ChrMapFactory, GeneFactory, PromoterRegionsFactory, \
    HarbisonChIPFactory, KemmerenTFKOFactory, BackgroundFactory, CCTFFactory, \
    CCExperimentFactory, HopsFactory, HopsReplicateSigFactory, \
    QcMetricsFactory, QcManualReviewFactory, QcR1ToR2TfFactory, \
    QcR2ToR1TfFactory, QcTfToTransposonFactory

fake = Faker()


# class TestUserListTestCase(APITestCase):
#     """
#     Tests /users list operations.
#     """

#     def setUp(self):
#         self.url = reverse('user-list')
#         self.user_data = factory.build(dict, FACTORY_CLASS=UserFactory)

#     def test_post_request_with_no_data_fails(self):
#         response = self.client.post(self.url, {})
#         eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_request_with_valid_data_succeeds(self):
#         response = self.client.post(self.url, self.user_data)
#         eq_(response.status_code, status.HTTP_201_CREATED)

#         user = User.objects.get(pk=response.data.get('id'))
#         eq_(user.username, self.user_data.get('username'))
#         ok_(check_password(self.user_data.get('password'), user.password))

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

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_request_updates_a_user(self):
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

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_request_updates_a_user(self):
        response = self.client.post(self.url, self.gene_data)
        assert response.status_code == status.HTTP_201_CREATED

        gene = Gene.objects.get(pk=response.data.get('id'))
        assert gene.systematic == self.gene_data.get('systematic')
        assert gene.uploader.username == self.user.username


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

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_request_updates_a_user(self):
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

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_request_updates_a_user(self):
        response = self.client.post(self.url, self.harbison_chip_data)
        assert response.status_code == status.HTTP_201_CREATED

        harbison_chip = HarbisonChIP.objects.get(pk=response.data.get('id'))
        assert harbison_chip.tf.pk == self.harbison_chip_data.get('tf')
        assert harbison_chip.uploader.username == self.user.username


#class TestKemmerenTFK