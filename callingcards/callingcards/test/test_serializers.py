from django.test import TestCase
from django.forms.models import model_to_dict

from callingcards.users.test.factories import UserFactory
from .factories import (ChrMapFactory, GeneFactory, PromoterRegionsFactory,
                        HarbisonChIPFactory, KemmerenTFKOFactory,
                        McIsaacZEVFactory, BackgroundFactory, CCTFFactory,
                        CCExperimentFactory, HopsFactory,
                        HopsReplicateSigFactory, QcMetricsFactory,
                        QcManualReviewFactory, QcR1ToR2TfFactory,
                        QcTfToTransposonFactory)

from ..serializers import (ChrMapSerializer, GeneSerializer,
                           PromoterRegionsSerializer,
                           PromoterRegionsTargetsOnlySerializer,
                           HarbisonChIPSerializer,
                           HarbisonChIPAnnotatedSerializer,
                           KemmerenTFKOSerializer, McIsaacZEVSerializer,
                           BackgroundSerializer, CCTFSerializer,
                           CCTFListSerializer,
                           CCExperimentSerializer, HopsSerializer,
                           HopsReplicateSigSerializer,
                           QcMetricsSerializer, QcManualReviewSerializer,
                           QcR1ToR2TfSerializer,
                           QcTfToTransposonSerializer,
                           ExpressionViewSetSerializer,
                           HopsReplicateSigAnnotatedSerializer)

from ..models import HarbisonChIP, PromoterRegions

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
        self.gene = GeneFactory(uploader=user, modifiedBy=user, chr=chr_record)
        self.promoter_region = PromoterRegionsFactory(
            modifiedBy=user,
            associated_feature=self.gene)
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
                'source': self.promoter_region.source
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


class TestHopsReplicateSig(TestCase):

    def setUp(self):
        pass

    def test_serializer_with_empty_data(self):
        serializer = HopsReplicateSigSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HopsReplicateSigSerializer(
            data=model_to_dict(HopsReplicateSigFactory.create()))
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


class TestHopsReplicateSigAnnotatedSerializer(TestCase):

    def setUp(self):
        user = UserFactory()
        chr_record = ChrMapFactory(uploader=user)
        gene_record_1 = GeneFactory(chr=chr_record, uploader=user)
        gene_record_2 = GeneFactory(chr=chr_record, uploader=user)
        cctf_record = CCTFFactory(uploader=user, tf=gene_record_1)
        experiment_record = CCExperimentFactory(uploader=user, tf=cctf_record)
        promoter_region = PromoterRegionsFactory(
            chr=chr_record, uploader=user, associated_feature=gene_record_2)
        hops_replicate_sig = HopsReplicateSigFactory(
            uploader=user, promoter=promoter_region, experiment=experiment_record)

        self.hops_replicate_sig_query_data = {
            'tf_id_alias': cctf_record.tf_id,
            'tf_locus_tag': gene_record_1.locus_tag,
            'tf_gene': gene_record_1.gene,
            'target_gene_id': gene_record_2.id,
            'target_locus_tag': gene_record_2.locus_tag,
            'target_gene': gene_record_2.gene,
            'bg_hops': hops_replicate_sig.bg_hops,
            'expr_hops': hops_replicate_sig.expr_hops,
            'poisson_pval': hops_replicate_sig.poisson_pval,
            'hypergeom_pval': hops_replicate_sig.hypergeom_pval,
            'experiment': experiment_record.id,
            'experiment_batch': experiment_record.batch,
            'experiment_batch_replicate': experiment_record.batch_replicate,
            'background': hops_replicate_sig.background,
            'promoter_id': promoter_region.id,
            'promoter_source': promoter_region.source,
        }

    def test_serializer_with_empty_data(self):
        serializer = HopsReplicateSigAnnotatedSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HopsReplicateSigAnnotatedSerializer(
            data=self.hops_replicate_sig_query_data)
        assert serializer.is_valid() is True
