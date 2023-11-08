import os
from django.test import override_settings
from django.test import TestCase
from django.forms.models import model_to_dict
from callingcards.users.test.factories import UserFactory
from .factories import (ChrMapFactory, GeneFactory, PromoterRegionsFactory,
                        PromoterRegionsSourceFactory,
                        ChipExoFactory,
                        HarbisonChIPFactory, KemmerenTFKOFactory,
                        McIsaacZEVFactory,
                        McIsaacZEV_s3Factory,
                        BackgroundFactory, CCTFFactory,
                        CCExperimentFactory, HopsFactory,
                        LabFactory,
                        QcMetricsFactory,
                        QcManualReviewFactory, QcR1ToR2TfFactory,
                        QcTfToTransposonFactory)

from ..serializers import (ChrMapSerializer, GeneSerializer,
                           PromoterRegionsSerializer,
                           PromoterRegionsTargetsOnlySerializer,
                           ChipExoSerializer, ChipExoAnnotatedSerializer,
                           HarbisonChIPSerializer,
                           HarbisonChIPAnnotatedSerializer,
                           KemmerenTFKOSerializer, McIsaacZEVSerializer,
                           McIsaacZEV_s3Serializer,
                           BackgroundSerializer, CCTFSerializer,
                           LabSerializer,
                           CCTFListSerializer,
                           CCExperimentSerializer, HopsSerializer,
                           QcMetricsSerializer, QcManualReviewSerializer,
                           QcR1ToR2TfSerializer,
                           QcTfToTransposonSerializer,
                           ExpressionViewSetSerializer)

from ..models import HarbisonChIP, PromoterRegions, ChipExo

TEST_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'test', 'data')


class TestCreateChrMap(TestCase):

    def setUp(self):
        self.serializer = ChrMapSerializer
        self.factory = ChrMapFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestGeneSerializer(TestCase):

    def setUp(self):
        self.serializer = GeneSerializer
        self.factory = GeneFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        data_dict = model_to_dict(self.factory.create())
        # since the record is already created, if we verify now it will fail
        # on the locus_tag field b/c it is not unique (it matches itself)
        serializer = self.serializer(
            data=data_dict)
        assert serializer.is_valid() is False
        # but if we change the locus tag, this will work
        data_dict['locus_tag'] = 'new_locus_tag'
        serializer = self.serializer(data=data_dict)
        assert serializer.is_valid() is True


class TestCreatePromoterRegions(TestCase):

    def setUp(self):
        self.serializer = PromoterRegionsSerializer
        self.factory = PromoterRegionsFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestPromoterRegionsTargetsOnly(TestCase):

    def setUp(self):
        user = UserFactory()
        chr_record = ChrMapFactory(uploader=user,
                                   modifiedBy=user)
        self.promoter_source = PromoterRegionsSourceFactory()
        self.gene = GeneFactory(uploader=user,
                                modifiedBy=user,
                                chr=chr_record)
        self.promoter_region = PromoterRegionsFactory(
            modifiedBy=user,
            associated_feature=self.gene,
            source=self.promoter_source)
        self.annotated_queryset = PromoterRegions.objects\
            .targets().filter(id=self.promoter_region.id)

    def test_serialization(self):
        serializer = PromoterRegionsTargetsOnlySerializer(
            self.annotated_queryset, many=True)
        serialized_data = serializer.data

        expected_data = [
            {
                'promoter_id': self.promoter_region.id,
                'target_gene_id': self.gene.id,
                'target_locus_tag': self.gene.locus_tag,
                'target_gene': self.gene.gene,
                'source': self.promoter_source.pk
            }
        ]

        self.assertEqual(serialized_data, expected_data)


class TestHarbisonChIP(TestCase):

    def setUp(self):
        user = UserFactory()
        chr_record = ChrMapFactory(uploader=user)
        gene_record = GeneFactory(uploader=user,
                                  chr=chr_record)
        self.harbisonchip_record = \
            HarbisonChIPFactory.build(uploader=user,
                                      gene=gene_record,
                                      tf=gene_record)
        self.harbison_data = model_to_dict(self.harbisonchip_record)  # noqa

    def test_serializer_with_empty_data(self):
        serializer = HarbisonChIPSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HarbisonChIPSerializer(data=self.harbison_data)  # noqa
        assert serializer.is_valid() is True

    def test_annotated_serializer_with_valid_data(self):
        self.harbisonchip_record.save()
        annotated_data = HarbisonChIP.objects.with_annotations()\
            .get(pk=self.harbisonchip_record.pk)
        serializer = HarbisonChIPAnnotatedSerializer(data=annotated_data)
        assert serializer.is_valid() is True


class TestChipExo(TestCase):

    def setUp(self):
        user = UserFactory()
        chr_record = ChrMapFactory(uploader=user)
        gene_record = GeneFactory(uploader=user,
                                  chr=chr_record)
        self.chipexo_record = \
            ChipExoFactory.build(uploader=user,
                                 gene=gene_record,
                                 tf=gene_record)
        self.chipexo_data = model_to_dict(self.chipexo_record)

    def test_serializer_with_empty_data(self):
        serializer = ChipExoSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = ChipExoSerializer(data=self.chipexo_data)  # noqa
        assert serializer.is_valid() is True

    def test_annotated_serializer_with_valid_data(self):
        self.chipexo_record.save()
        annotated_data = ChipExo.objects.with_annotations()\
            .get(pk=self.chipexo_record.pk)
        serializer = ChipExoAnnotatedSerializer(data=annotated_data)
        assert serializer.is_valid() is True


class TestKemmerenTFKO(TestCase):

    def setUp(self):
        self.serializer = KemmerenTFKOSerializer
        self.factory = KemmerenTFKOFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestMcIsaacZEV(TestCase):

    def setUp(self):
        self.serializer = McIsaacZEVSerializer
        self.factory = McIsaacZEVFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class TestMcIsaacZEV_s3(TestCase):

    def setUp(self):
        self.serializer = McIsaacZEV_s3Serializer
        self.factory = McIsaacZEV_s3Factory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True

class TestBackground(TestCase):

    def setUp(self):
        self.serializer = BackgroundSerializer
        self.factory = BackgroundFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestCCTF(TestCase):

    def setUp(self):
        self.serializer = CCTFSerializer
        self.factory = CCTFFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestCCTFListSerializer(TestCase):

    def setUp(self):
        user = UserFactory()
        chr_record = ChrMapFactory(uploader=user,
                                   modifiedBy=user)
        gene_record = GeneFactory(uploader=user,
                                  modifiedBy=user,
                                  chr=chr_record)

        self.cctf_list_data = {
            "tf_id": gene_record.id,
            "tf_locus_tag": gene_record.locus_tag,
            "tf_gene": gene_record.gene}

    def test_serializer_with_empty_data(self):
        serializer = CCTFListSerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_valid_data(self):
        serializer = CCTFListSerializer(data=self.cctf_list_data)
        self.assertTrue(serializer.is_valid())


class TestCCExperiment(TestCase):

    def setUp(self):
        self.serializer = CCExperimentSerializer
        self.factory = CCExperimentFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestLab(TestCase):

    def setUp(self):
        self.serializer = LabSerializer
        self.factory = LabFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.build()))
        assert serializer.is_valid() is True


class TestHops(TestCase):

    def setUp(self):
        pass

    def test_serializer_with_empty_data(self):
        serializer = HopsSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HopsSerializer(
            data=model_to_dict(HopsFactory.create()))
        assert serializer.is_valid() is True


class TestQcMetrics(TestCase):

    def setUp(self):
        pass

    def test_serializer_with_empty_data(self):
        serializer = QcMetricsSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = QcMetricsSerializer(
            data=model_to_dict(QcMetricsFactory.create()))
        assert serializer.is_valid() is True


class TestQcManifest(TestCase):

    def setUp(self):
        self.serializer = QcManualReviewSerializer
        self.factory = QcManualReviewFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestQcR1ToR2Tf(TestCase):

    def setUp(self):
        self.serializer = QcR1ToR2TfSerializer
        self.factory = QcR1ToR2TfFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class TestQcTfToTransposon(TestCase):

    def setUp(self):
        self.serializer = QcTfToTransposonSerializer
        self.factory = QcTfToTransposonFactory

    def test_serializer_with_empty_data(self):
        serializer = self.serializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(
            data=model_to_dict(self.factory.create()))
        assert serializer.is_valid() is True


class ExpressionViewSetSerializerTestCase(TestCase):

    def setUp(self):
        self.serializer = ExpressionViewSetSerializer()

    def test_serializer_with_valid_data(self):
        data = {
            'tf_alias': 1,
            'tf_locus_tag': 'yhr123',
            'tf_gene': 'tf_gene',
            'target_gene_id': 2,
            'target_locus_tag': 'yhr456',
            'target_gene': 'target_gene',
            'effect_expr': 0.5,
            'p_expr': 0.01,
            'source_expr': 'test'
        }

        self.assertEqual(self.serializer.validate(data), data)

    def test_serializer_with_invalid_data(self):
        data = {
            'tf_alias': 123,
            'effect_expr': 'invalid',
            'p_expr': -100,
            'source_expr': 123
        }
        serializer = ExpressionViewSetSerializer(data=data)
        assert serializer.is_valid() is False
