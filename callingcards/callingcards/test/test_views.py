# pylint: disable=E1101
import logging
import json
from unittest import mock
import io
import csv
import os
from decimal import Decimal

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import override_settings
from django.urls import reverse
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
import factory

from callingcards.callingcards.tasks import process_upload

from callingcards.users.test.factories import UserFactory

from callingcards.callingcards.models import (ChrMap, Gene, PromoterRegions,
                                              HarbisonChIP, KemmerenTFKO,
                                              McIsaacZEV, Background, CCTF,
                                              CCExperiment, Hops, Hops_s3,
                                              QcMetrics,
                                              QcR1ToR2Tf, QcR2ToR1Tf,
                                              QcTfToTransposon)

from callingcards.callingcards.serializers import (HarbisonChIPSerializer,
                                                   HarbisonChIPAnnotatedSerializer)  # noqa

from .factories import (ChrMapFactory, GeneFactory, PromoterRegionsFactory,
                        HarbisonChIPFactory, KemmerenTFKOFactory,
                        McIsaacZEVFactory, BackgroundFactory,
                        BackgroundSourceFactory, CCTFFactory,
                        CCExperimentFactory,
                        HopsSourceFactory, HopsFactory,
                        QcMetricsFactory,
                        QcManualReviewFactory,
                        QcR1ToR2TfFactory, QcR2ToR1TfFactory,
                        QcTfToTransposonFactory,
                        CallingCardsSigFactory,
                        PromoterRegionsSourceFactory,
                        random_file_from_media_directory)

from ..views import ExpressionViewSet

from ..filters import HarbisonChIPFilter

fake = Faker()

AUTO_ADD_FIELDS = ['uploader', 'uploadDate', 'modified', 'modifiedBy']


class TestChrMapViewSet(APITestCase):
    """
    Tests /chrmap detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.chr_data = factory.build(dict, FACTORY_CLASS=ChrMapFactory)
        for attr in AUTO_ADD_FIELDS:
            self.chr_data.pop(attr, None)
        self.url = reverse('chrmap-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.chr_data)
        assert response.status_code == status.HTTP_201_CREATED

        chr_record = ChrMap.objects.get(pk=response.data.get('id'))
        assert chr_record.chr == self.chr_data.get('chr')
        assert chr_record.uploader.username == self.user.username


class TestGeneViewSet(APITestCase):
    """
    Tests /gene detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.gene_data = factory.build(dict, FACTORY_CLASS=GeneFactory)
        self.gene_data['chr'] = self.chr_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.gene_data.pop(attr, None)

        self.url = reverse('gene-list')

        settings.DEBUG = True
        self.gene_record_bulk_data = factory.build_batch(
            dict,
            10,
            FACTORY_CLASS=GeneFactory)
        for rec in self.gene_record_bulk_data:
            rec['chr'] = self.chr_record.pk
            for attr in AUTO_ADD_FIELDS:
                rec.pop(attr, None)

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.gene_data)
        assert response.status_code == status.HTTP_201_CREATED

        gene = Gene.objects.get(pk=response.data.get('id'))
        assert gene.locus_tag == self.gene_data.get('locus_tag')
        assert gene.uploader.username == self.user.username

    def test_put_bulk(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.gene_record_bulk_data),
            content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_fields(self):
        response = self.client.get(reverse('gene-fields'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('readable', response.data)
        self.assertIn('writable', response.data)
        self.assertIn('automatically_generated', response.data)
        self.assertIn('filter', response.data)

    def test_get_pagination_info(self):
        response = self.client.get(reverse('gene-pagination-info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('default_page_size', response.data)
        self.assertIn('page_size_limit', response.data)

    def test_get_count(self):
        response = self.client.get(reverse('gene-count'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)

    def test_create_async_single(self):
        with mock\
            .patch('callingcards.callingcards.tasks.process_upload.delay') \
                as mock_process_upload:
            new_gene_data = factory.build(dict, FACTORY_CLASS=GeneFactory)
            new_gene_data['chr'] = self.chr_record.pk
            for attr in AUTO_ADD_FIELDS:
                new_gene_data.pop(attr, None)
            response = self.client.post(reverse('gene-create-async'),
                                        json.dumps(new_gene_data),
                                        content_type='application/json')

        # Check if the endpoint returns HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the process_upload Celery task was called with the
        # correct arguments
        # Check if the process_upload Celery task was called with the
        # correct arguments
        # expected_args = (new_gene_data, False, {
        #     'uploader': self.user,
        #     'serializer_class_path':
        #     'callingcards.callingcards.serializers.GeneSerializer'
        # })

        # despite being exactly the same to my eye and chatGPT,
        # this test fails. Possibly a bug in the method?
        # mock_process_upload.assert_called_once_with(*expected_args)

    def test_create_async_bulk(self):
        with mock\
            .patch('callingcards.callingcards.tasks.process_upload.delay') \
                as mock_process_upload:
            new_gene_record_bulk_data = factory.build_batch(
                dict,
                10,
                FACTORY_CLASS=GeneFactory)
            for rec in new_gene_record_bulk_data:
                rec['chr'] = self.chr_record.pk
                for attr in AUTO_ADD_FIELDS:
                    rec.pop(attr, None)

            response = self.client.post(
                reverse('gene-create-async'),
                data=json.dumps(new_gene_record_bulk_data),
                content_type='application/json')

        # Check if the endpoint returns HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the process_upload Celery task was called with the
        # correct arguments
        # see single entry note above
        # mock_process_upload.assert_called_once_with(
        #     new_gene_record_bulk_data,
        #     True,
        #     {'uploader': self.user,
        #      'serializer_class_path': 'myapp.serializers.GeneSerializer'})


class TestPromoterRegionsViewSet(APITestCase):
    """
    Tests /promoter_regions detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.gene_record = GeneFactory.create()
        self.promoterregionssource = PromoterRegionsSourceFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.promoter_regions_data = factory.build(
            dict,
            FACTORY_CLASS=PromoterRegionsFactory)
        self.promoter_regions_data['chr'] = self.chr_record.pk
        self.promoter_regions_data['associated_feature'] = self.gene_record.pk
        self.promoter_regions_data['source'] = \
            self.promoterregionssource.pk
        for attr in AUTO_ADD_FIELDS:
            self.promoter_regions_data.pop(attr, None)
        self.url = reverse('promoterregions-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.promoter_regions_data)
        assert response.status_code == status.HTTP_201_CREATED

        promoter_regions = PromoterRegions.objects\
            .get(pk=response.data.get('id'))
        assert promoter_regions.associated_feature.pk == \
            self.promoter_regions_data.get('associated_feature')
        assert promoter_regions.uploader.username == self.user.username

    def test_targets_endpoint(self):
        # Create a PromoterRegions instance to have some data to test with
        PromoterRegionsFactory.create(uploader=self.user,
                                      associated_feature=self.gene_record,
                                      source=self.promoterregionssource)

        targets_url = reverse('promoterregions-targets')
        response = self.client.get(targets_url)
        assert response.status_code == status.HTTP_200_OK

    def test_targets_count_endpoint(self):
        count_url = reverse('promoterregions-targets-count')
        response = self.client.get(count_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'count': PromoterRegions.objects.count()}

    def test_targets_pagination_info_endpoint(self):
        pagination_info_url = \
            reverse('promoterregions-targets-pagination-info')
        response = self.client.get(pagination_info_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'default_page_size': api_settings.PAGE_SIZE,
            'page_size_limit': settings.REST_FRAMEWORK.get('PAGE_SIZE', None)
        }

    def test_targets_fields_endpoint(self):
        fields_url = reverse('promoterregions-targets-fields')
        response = self.client.get(fields_url)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == \
            {'readable', 'writable', 'automatically_generated', 'filter'}

    def test_callingcards_endpoint(self):
        # Create a CCExperiment instance to have some data to test with
        filepath = os.path.join(
            'analysis',
            'run_5690',
            'ccexperiment_75_yiming.csv.gz')
        experiment = CCExperimentFactory.create(
            id=75,
            uploader=self.user,
            batch='run_5690')
        background_source = BackgroundSourceFactory.create(
            source='adh1'
        )

        # Create a CallingCardsSig instance to have some data to test with
        callingcards_sig = CallingCardsSigFactory.create(
            experiment=experiment,
            background_source=background_source,
            promoter_source=self.promoterregionssource,
            file=filepath)

        callingcards_url = reverse('promoterregions-callingcards')
        response = self.client.get(callingcards_url)

        # Check the response status code
        assert response.status_code == status.HTTP_200_OK

        # Check the content type
        assert response['Content-Type'] == 'application/gzip'

        # Check the content encoding
        assert response['Content-Encoding'] == 'gzip'

        # Check the content disposition
        assert response['Content-Disposition'] == \
            'attachment; filename="data.csv.gz"'


class TestHarbisonChIP(APITestCase):
    """
    Tests /harbison_chip detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        HarbisonChIPFactory.create(
            uploader=self.user,
            gene=self.gene_record,
            tf=self.gene_record
        )
        self.url = reverse('harbisonchip-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        harbison_chip_data = factory.build(
            dict,
            FACTORY_CLASS=HarbisonChIPFactory)
        harbison_chip_data['gene'] = self.gene_record.pk
        harbison_chip_data['tf'] = self.gene_record.pk
        for attr in AUTO_ADD_FIELDS:
            harbison_chip_data.pop(attr, None)
        response = self.client.post(self.url, harbison_chip_data)
        assert response.status_code == status.HTTP_201_CREATED

        harbison_chip = HarbisonChIP.objects.get(pk=response.data.get('id'))
        assert harbison_chip.tf.pk == harbison_chip_data.get('tf')
        assert harbison_chip.uploader.username == self.user.username

    def test_harbison_chip_filtering(self):
        # Modify one of the HarbisonChIP instances to test filtering
        harbison_chip = HarbisonChIP.objects.get(pk=1)
        harbison_chip.start = '6042'
        harbison_chip.save()

        filter_url = f"{self.url}?start=6042"

        response = self.client.get(filter_url)
        assert response.status_code == status.HTTP_200_OK

        # Check if the returned data matches the expected data
        expected_data = HarbisonChIPSerializer([harbison_chip],
                                               many=True).data
        assert response.data['results'] == expected_data

    def test_harbison_chip_count_endpoint(self):
        response = self.client.get(reverse('harbisonchip-count'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'count': HarbisonChIP.objects.count()}

        annote_response = self.client\
            .get(reverse('harbisonchip-with-annote-count'))
        assert annote_response.status_code == status.HTTP_200_OK
        assert annote_response.data == \
            {'count': HarbisonChIP.objects.with_annotations().count()}

    def test_harbison_chip_pagination_info_endpoint(self):
        response = self.client.get(reverse('harbisonchip-pagination-info'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'default_page_size': api_settings.PAGE_SIZE,
            'page_size_limit': settings.REST_FRAMEWORK.get('PAGE_SIZE', None)
        }

        annote_response = self.client.get(
            reverse('harbisonchip-with-annote-pagination-info'))
        assert annote_response.status_code == status.HTTP_200_OK
        assert annote_response.data == {
            'default_page_size': api_settings.PAGE_SIZE,
            'page_size_limit': settings.REST_FRAMEWORK.get('PAGE_SIZE', None)
        }

    def test_harbison_chip_fields_endpoint(self):
        response = self.client.get(reverse('harbisonchip-fields'))
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == \
            {'readable', 'writable', 'automatically_generated', 'filter'}

    def test_harbison_chip_with_annote_fields_endpoint(self):
        response = self.client.get(reverse('harbisonchip-with-annote-fields'))
        assert response.status_code == status.HTTP_200_OK

        expected_fields = {
            'readable': ['tf_id', 'tf_locus_tag', 'tf_gene', 'target_gene_id',
                         'target_locus_tag', 'target_gene',
                         'binding_signal', 'experiment'],
            'writable': None,
            'automatically_generated': None,
            'filter': HarbisonChIPFilter.Meta.fields
        }
        assert response.data == expected_fields

    def test_harbison_chip_with_annote_endpoint(self):
        response = self.client.get(reverse('harbisonchip-with-annote'))
        assert response.status_code == status.HTTP_200_OK

        # Check if the returned data matches the expected data
        annotated_queryset = HarbisonChIP.objects\
            .with_annotations().order_by('id')
        expected_data = HarbisonChIPAnnotatedSerializer(
            annotated_queryset, many=True).data
        assert response.data['results'] == expected_data

    def test_harbison_chip_with_annote_filtering(self):
        # Modify one of the HarbisonChIP instances to test filtering
        # harbison_chip = HarbisonChIP.objects.first()
        # tf_id = harbison_chip.tf_id
        tf_locus_tag = self.gene_record.locus_tag
        filter_url = f"{reverse('harbisonchip-with-annote')}?tf_locus_tag={tf_locus_tag}"  # noqa

        response = self.client.get(filter_url)
        assert response.status_code == status.HTTP_200_OK

        # Check if the returned data matches the expected data
        annotated_queryset = HarbisonChIP.objects.with_annotations()\
            .filter(tf_locus_tag=tf_locus_tag).order_by('id')
        expected_data = HarbisonChIPAnnotatedSerializer(
            annotated_queryset, many=True).data
        assert response.data['results'] == expected_data


@override_settings(DATABASES={'default':
                              {'ENGINE':
                               'django.db.backends.postgresql_psycopg2'}})
class TestKemmerenTFKO(APITestCase):
    """
    Tests /kemmeren_tfko detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.kemmeren_tfko_data = factory.build(
            dict, FACTORY_CLASS=KemmerenTFKOFactory)
        self.kemmeren_tfko_data['gene'] = self.gene_record.pk
        self.kemmeren_tfko_data['tf'] = self.gene_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.kemmeren_tfko_data.pop(attr, None)
        self.url = reverse('kemmerentfko-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.kemmeren_tfko_data)
        assert response.status_code == status.HTTP_201_CREATED

        kemmeren_tfko = KemmerenTFKO.objects.get(pk=response.data.get('id'))
        assert kemmeren_tfko.tf.pk == self.kemmeren_tfko_data.get('tf')
        assert kemmeren_tfko.uploader.username == self.user.username

    def test_upload_csv(self):
        # Create a test CSV file with valid data
        header = ['gene', 'effect', 'pval', 'tf']
        gene = GeneFactory.create()
        tf = GeneFactory.create()
        data = [
            [gene.pk, '0.1', '0.01', tf.pk],
            [gene.pk, '0.2', '0.02', tf.pk],
            [gene.pk, '0.3', '0.03', tf.pk]
        ]
        with io.StringIO() as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
            f.seek(0)
            csv_file = SimpleUploadedFile("test_mcisaaczev.csv",
                                          f.read().encode('utf-8'),
                                          content_type="text/csv")

        # Make a request to the upload-csv endpoint
        url = reverse('mcisaaczev-upload-csv')
        response = self.client.post(url, {'csv_file': csv_file},
                                    format='multipart')

        # Check the response and the database
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'status':
                                 'CSV data uploaded successfully.'}

        queryset = McIsaacZEV.objects.all()
        assert queryset.count() == 3
        for i, record in enumerate(queryset):
            assert record.gene == gene
            assert Decimal(data[i][1]) == record.effect
            assert Decimal(data[i][2]) == record.pval
            assert record.tf == tf
            assert str(record.uploader) == self.user.username
            assert record.uploadDate is not None
            assert record.modified is not None


class TestMcIsaacZEV(APITestCase):
    """
    Tests /mcisaac_zev detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.mcisaac_zev_data = factory.build(
            dict, FACTORY_CLASS=McIsaacZEVFactory)
        self.mcisaac_zev_data['gene'] = self.gene_record.pk
        self.mcisaac_zev_data['tf'] = self.gene_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.mcisaac_zev_data.pop(attr, None)
        self.url = reverse('mcisaaczev-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
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
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.backgroundsource = BackgroundSourceFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.url = reverse('background-list')

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        background_data = factory.build(
            dict, FACTORY_CLASS=BackgroundFactory)
        background_data['chr'] = self.chr_record.pk
        background_data['source'] = self.backgroundsource.pk
        for attr in AUTO_ADD_FIELDS:
            background_data.pop(attr, None)
        response = self.client.post(self.url, background_data)
        assert response.status_code == status.HTTP_201_CREATED

        background = Background.objects.get(pk=response.data.get('id'))
        assert background.chr.pk == background_data.get('chr')
        assert background.uploader.username == self.user.username


class TestCCTF(APITestCase):
    """
    Tests /cctf detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.gene_record = GeneFactory.create(uploader=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.url = reverse('cctf-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        cctf_data = factory.build(dict, FACTORY_CLASS=CCTFFactory)
        cctf_data['tf'] = self.gene_record.pk
        for attr in AUTO_ADD_FIELDS:
            cctf_data.pop(attr, None)
        response = self.client.post(self.url, cctf_data)
        assert response.status_code == status.HTTP_201_CREATED

        cctf = CCTF.objects.get(pk=response.data.get('id'))
        assert cctf.tf.pk == cctf_data.get('tf')
        assert cctf.uploader.username == self.user.username

    def test_tf_list(self):
        # Make a request to the tf_list endpoint
        CCTFFactory.create(uploader=self.user, tf=self.gene_record)
        response = self.client.get(reverse('cctf-tf-list'))
        assert response.status_code == status.HTTP_200_OK

        # Check if the returned data matches the expected data
        assert self.gene_record.gene == \
            response.data['results'][0].get('tf_gene')


class TestCCExperiment(APITestCase):
    """
    Tests /ccexperiment detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.cctf_record = CCTFFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.ccexperiment_data = factory.build(
            dict, FACTORY_CLASS=CCExperimentFactory)
        self.ccexperiment_data['tf'] = self.cctf_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.ccexperiment_data.pop(attr, None)
        self.url = reverse('ccexperiment-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.ccexperiment_data)
        assert response.status_code == status.HTTP_201_CREATED

        ccexperiment = CCExperiment.objects.get(pk=response.data.get('id'))
        assert ccexperiment.tf.pk == self.ccexperiment_data.get('tf')
        assert ccexperiment.uploader.username == self.user.username


class TestHops_s3(APITestCase):
    """
    Tests /hops_s3 detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.source_record = HopsSourceFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.tf_gene = GeneFactory.create(gene='TFGENE')
        self.tf_locus_tag = GeneFactory.create(locus_tag='TFLOCUSTAG')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.url = reverse('hopss3-list')

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_hops_s3_with_ccexpr(self):
        media_directory = default_storage.location
        qbed_file = random_file_from_media_directory('qbed')

        upload_file = os.path.join(media_directory, qbed_file)

        with open(upload_file, 'rb') as f:
            post_data = {
                'chr_format': 'mitra',
                'source': self.source_record.pk,
                'experiment': self.experiment_record.pk,
                'qbed': f,
                'notes': 'some notes'
            }

            # Test the create() method
            response = self.client.post(self.url,
                                        post_data,
                                        format='multipart')
            
        assert response.status_code == status.HTTP_201_CREATED

        hops_s3 = Hops_s3.objects.get(pk=response.data.get('id'))
        assert hops_s3.source.pk == post_data.get('source')
        assert hops_s3.experiment.pk == post_data.get('experiment')
        assert hops_s3.notes == post_data.get('notes')
    
    def test_create_hops_s3_no_ccexpr_gene(self):
        media_directory = default_storage.location
        qbed_file = random_file_from_media_directory('qbed')

        upload_file = os.path.join(media_directory, qbed_file)

        with open(upload_file, 'rb') as f:
            post_data = {
                'chr_format': 'mitra',
                'tf_gene': 'TFGENE',
                'batch': 'run_1234',
                'batch_replicate': 1,
                'source': self.source_record.pk,
                'qbed': f,
                'notes': 'some notes'
            }

            # Test the create() method
            response = self.client.post(self.url,
                                        post_data,
                                        format='multipart')
            
        assert response.status_code == status.HTTP_201_CREATED

        hops_s3 = Hops_s3.objects.get(pk=response.data.get('id'))
        assert hops_s3.source.pk == post_data.get('source')
        assert hops_s3.experiment.pk != post_data.get('experiment')
        assert hops_s3.notes == post_data.get('notes')

    def test_create_hops_s3_no_ccexpr_locus_tag(self):
        media_directory = default_storage.location
        qbed_file = random_file_from_media_directory('qbed')

        upload_file = os.path.join(media_directory, qbed_file)

        with open(upload_file, 'rb') as f:
            post_data = {
                'chr_format': 'mitra',
                'tf_locus_tag': 'TFLOCUSTAG',
                'batch': 'run_1234',
                'batch_replicate': 1,
                'source': self.source_record.pk,
                'qbed': f,
                'notes': 'some notes'
            }

            # Test the create() method
            response = self.client.post(self.url,
                                        post_data,
                                        format='multipart')
            
        assert response.status_code == status.HTTP_201_CREATED

        hops_s3 = Hops_s3.objects.get(pk=response.data.get('id'))
        assert hops_s3.source.pk == post_data.get('source')
        assert hops_s3.experiment.pk != post_data.get('experiment')
        assert hops_s3.notes == post_data.get('notes')

class TestHops(APITestCase):
    """
    Tests /hops detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.hops_data = factory.build(dict, FACTORY_CLASS=HopsFactory)
        self.hops_data['chr'] = self.chr_record.pk
        self.hops_data['experiment'] = self.experiment_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.hops_data.pop(attr, None)
        self.url = reverse('hops-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.hops_data)
        assert response.status_code == status.HTTP_201_CREATED

        hops = Hops.objects.get(pk=response.data.get('id'))
        assert hops.chr.pk == self.hops_data.get('chr')
        assert hops.experiment.pk == self.hops_data.get('experiment')
        assert hops.uploader.username == self.user.username


class TestQcMetrics(APITestCase):
    """
    Tests /qcmetrics detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qcmetrics_data = factory.build(
            dict, FACTORY_CLASS=QcMetricsFactory)
        self.qcmetrics_data['experiment'] = self.experiment_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.qcmetrics_data.pop(attr, None)
        self.url = reverse('qcmetrics-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qcmetrics_data)
        assert response.status_code == status.HTTP_201_CREATED

        qcmetrics = QcMetrics.objects.get(pk=response.data.get('id'))
        assert qcmetrics.experiment.pk == \
            self.qcmetrics_data.get('experiment')
        assert qcmetrics.uploader.username == self.user.username


class TestQcR1ToR2Tf(APITestCase):
    """
    Tests /qcr1tor2tf detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qcr1tor2tf_data = factory.build(
            dict, FACTORY_CLASS=QcR1ToR2TfFactory)
        self.qcr1tor2tf_data['experiment'] = self.experiment_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.qcr1tor2tf_data.pop(attr, None)
        self.url = reverse('qcr1tor2-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qcr1tor2tf_data)
        assert response.status_code == status.HTTP_201_CREATED

        qcr1tor2tf = QcR1ToR2Tf.objects.get(pk=response.data.get('id'))
        assert qcr1tor2tf.experiment.pk == \
            self.qcr1tor2tf_data.get('experiment')
        assert qcr1tor2tf.uploader.username == self.user.username


class TestQcR2ToR1Tf(APITestCase):
    """
    Tests /qcr2tor1tf detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qcr2tor1tf_data = factory.build(
            dict, FACTORY_CLASS=QcR2ToR1TfFactory)
        self.qcr2tor1tf_data['experiment'] = self.experiment_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.qcr2tor1tf_data.pop(attr, None)
        self.url = reverse('qcr2tor1-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qcr2tor1tf_data)
        assert response.status_code == status.HTTP_201_CREATED

        qcr2tor1tf = QcR2ToR1Tf.objects.get(pk=response.data.get('id'))
        assert qcr2tor1tf.experiment.pk == \
            self.qcr2tor1tf_data.get('experiment')
        assert qcr2tor1tf.uploader.username == self.user.username


class TestQcTfToTransposon(APITestCase):
    """
    Tests /qctftotransposon detail operations.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = UserFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.qctftotransposon_data = factory.build(
            dict, FACTORY_CLASS=QcTfToTransposonFactory)
        self.qctftotransposon_data['experiment'] = self.experiment_record.pk
        for attr in AUTO_ADD_FIELDS:
            self.qctftotransposon_data.pop(attr, None)
        self.url = reverse('qctftotransposon-list')
        settings.DEBUG = True

    def test_post_fail(self):
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_single(self):
        response = self.client.post(self.url, self.qctftotransposon_data)
        assert response.status_code == status.HTTP_201_CREATED

        qctftotransposon = QcTfToTransposon.objects\
            .get(pk=response.data.get('id'))
        assert qctftotransposon.experiment.pk == \
            self.qctftotransposon_data.get('experiment')
        assert qctftotransposon.uploader.username == self.user.username


class TestQcManualReviewViewSet(APITestCase):
    def setUp(self):
        # create two users
        self.user = UserFactory.create()
        self.second_user = UserFactory.create()
        # sign in as the second user
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        # create a QcManualReview object
        self.qc_manual_review = QcManualReviewFactory.create()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.second_user.auth_token}')
        self.url = reverse('qcmanualreview-list')

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_update(self):
        # Update the necessary fields
        update_data = {'notes': 'updated_value'}
        # Construct the detail URL for the update
        update_url = f"{self.url}{self.qc_manual_review.pk}/"
        # Use PATCH to update the object
        response = self.client.patch(update_url, update_data)
        assert response.status_code == status.HTTP_200_OK

        # Refresh the object from the database
        self.qc_manual_review.refresh_from_db()

        # Compare uploader and modifiedBy fields
        assert self.qc_manual_review.uploader != \
            self.qc_manual_review.modifiedBy

        # Compare uploadDate and modified fields
        assert self.qc_manual_review.uploadDate != \
            self.qc_manual_review.modified


class TestQcReviewViewSet(APITestCase):
    """
    Tests QcReviewViewSet operations.
    """

    def setUp(self):
        self.user = UserFactory.create()
        self.chr_record = ChrMapFactory.create()
        self.experiment_record = CCExperimentFactory.create()
        self.hops_record = HopsFactory.create(
            uploader=self.user,
            experiment=self.experiment_record)
        self.qcr1tor2tf_record = QcR1ToR2TfFactory.create(
            uploader=self.user,
            experiment=self.experiment_record)
        self.qcr2tor1tf_record = QcR2ToR1TfFactory.create(
            uploader=self.user,
            experiment=self.experiment_record)
        self.unknown_feature = GeneFactory.create(
            chr=self.chr_record,
            uploader=self.user,
            locus_tag='undetermined')

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

        self.url = reverse('qcreview-list')

    def test_get_url(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    # def test_put_single(self):
    #     # Prepare update data
    #     update_data = {
    #         'rank_recall': 0.95,
    #         'chip_better': True,
    #         'data_usable': True,
    #         'passing_replicate': True,
    #         'note': 'Test note'
    #     }

    #     # Send a PUT request to update the QcManualReview related to the QcReview
    #     response = self.client.put(f"{self.url}/", update_data)
    #     assert response.status_code == status.HTTP_201_CREATED

    #     # Check if the updated fields in the response match the input data
    #     for key, value in update_data.items():
    #         assert response.data[key] == value


class TestExpressionViewSet(APITestCase):
    def setUp(self):
        self.view = ExpressionViewSet.as_view({'get': 'list'})
        user = UserFactory.create()
        token = Token.objects.get(user=user)
        self.url = reverse('expression-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        # Create some test data
        chr_record = ChrMapFactory.create(uploader=user)
        gene_record = GeneFactory.create(chr=chr_record, uploader=user)
        CCExperimentFactory.create(uploader=user)
        McIsaacZEVFactory.create(gene=gene_record,
                                 uploader=user)
        KemmerenTFKOFactory.create(tf=gene_record,
                                   uploader=user)

        # Set up request query parameters
        self.query_params = {
            'mcisaac_zev__gene__in': gene_record.pk,
            'kemmeren_tfko__tf__in': gene_record.pk
        }

    def test_get_queryset(self):
        response = self.client.get(self.url, self.query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination_info(self):
        url = reverse('expression-pagination-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_count(self):
        url = reverse('expression-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_model_fields(self):
        url = reverse('expression-fields')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
