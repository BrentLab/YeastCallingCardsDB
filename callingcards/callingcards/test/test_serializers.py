import pytest
from django.test import TestCase
from django.forms.models import model_to_dict

from callingcards.users.test.factories import UserFactory
from .factories import *  # pylint: disable=W0401,W0614 # noqa
from ..serializers import *  # pylint: disable=W0401,W0614 # noqa


class TestCreateChrMap(TestCase):

    def setUp(self):
        user = UserFactory()
        self.chrmap_data = model_to_dict(ChrMapFactory.build(uploader=user))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = ChrMapSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = ChrMapSerializer(data=self.chrmap_data)  # noqa
        assert serializer.is_valid() is True


class TestCreateGene(TestCase):

    def setUp(self):
        # note that this instantiates and saves to the DB
        # must set systematic to something unique as a result
        # probably worth a post to github
        chr_record = ChrMapFactory()
        self.gene_data = model_to_dict(GeneFactory.build(chr=chr_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = GeneSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = GeneSerializer(data=self.gene_data)  # noqa
        assert serializer.is_valid() is True

class TestCreatePromoterRegions(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        self.promoter_data = model_to_dict(
            PromoterRegionsFactory.build(chr=chr_record,
                                         associated_feature=gene_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = PromoterRegionsSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = PromoterRegionsSerializer(data=self.promoter_data)  # noqa
        assert serializer.is_valid() is True

class TestHarbisonChIP(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)

        self.harbison_data = model_to_dict(
            HarbisonChIPFactory.build(gene=gene_record,
                                      tf=gene_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = HarbisonChIPSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HarbisonChIPSerializer(data=self.harbison_data)  # noqa
        assert serializer.is_valid() is True


class TestKemmerenTFKO(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)

        self.kemmeren_data = model_to_dict(
            KemmerenTFKOFactory.build(gene=gene_record,
                                      tf=gene_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = KemmerenTFKOSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = KemmerenTFKOSerializer(data=self.kemmeren_data)  # noqa
        assert serializer.is_valid() is True


class TestMcIsaacZEV(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)

        self.mcisaac_data = model_to_dict(
            McIsaacZEVFactory.build(gene=gene_record,
                                    tf=gene_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = McIsaacZEVSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = McIsaacZEVSerializer(data=self.mcisaac_data)  # noqa
        assert serializer.is_valid() is True


class TestBackground(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()

        self.background_data = model_to_dict(
            BackgroundFactory.build(chr=chr_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = BackgroundSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = BackgroundSerializer(data=self.background_data)  # noqa
        assert serializer.is_valid() is True


class TestCCTF(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)

        self.cctf_data = model_to_dict(
            CCTFFactory.build(tf=gene_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = CCTFSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = CCTFSerializer(data=self.cctf_data)  # noqa
        assert serializer.is_valid() is True


class TestCCExperiment(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)

        self.ccexp_data = model_to_dict(
            CCExperimentFactory.build(tf=cctf_record))  # noqa

    def test_serializer_with_empty_data(self):
        serializer = CCExperimentSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = CCExperimentSerializer(data=self.ccexp_data)  # noqa
        assert serializer.is_valid() is True


class TestHops(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.hops_data = model_to_dict(HopsFactory.build(  # noqa
            chr=chr_record, experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = HopsSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HopsSerializer(data=self.hops_data)  # noqa
        assert serializer.is_valid() is True


class TestHopsReplicateSig(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.hops_rep_data = model_to_dict(HopsReplicateSigFactory.build(  # noqa
            chr=chr_record, experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = HopsReplicateSigSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = HopsReplicateSigSerializer(data=self.hops_rep_data)  # noqa
        assert serializer.is_valid() is True


class TestQcMetrics(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.qc_data = model_to_dict(QcMetricsFactory.build(  # noqa
            experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = QcMetricsSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = QcMetricsSerializer(data=self.qc_data)  # noqa
        assert serializer.is_valid() is True


class TestQcManifest(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.qc_manifest_data = model_to_dict(QcManualReviewFactory.build(  # noqa
            experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = QcManualReviewSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = QcManualReviewSerializer(data=self.qc_manifest_data)  # noqa
        assert serializer.is_valid() is True


class TestQcR1ToR2Tf(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.qc_r1_to_r2_data = model_to_dict(QcR1ToR2TfFactory.build(  # noqa
            experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = QcR1ToR2TfSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = QcR1ToR2TfSerializer(data=self.qc_r1_to_r2_data)  # noqa
        assert serializer.is_valid() is True


class TestQcR1ToR2Tf(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.qc_r1_to_r2_data = model_to_dict(QcR1ToR2TfFactory.build(  # noqa
            experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = QcR1ToR2TfSerializer(data={})  # noqa
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = QcR1ToR2TfSerializer(data=self.qc_r1_to_r2_data)  # noqa
        assert serializer.is_valid() is True


class TestQcTfToTransposon(TestCase):

    def setUp(self):
        chr_record = ChrMapFactory()
        gene_record = GeneFactory(chr=chr_record)
        cctf_record = CCTFFactory(tf=gene_record)
        expr_record = CCExperimentFactory(tf=cctf_record)

        self.qc_tf_to_transposon_data = model_to_dict(  # noqa
            QcTfToTransposonFactory.build(experiment=expr_record))

    def test_serializer_with_empty_data(self):
        serializer = QcTfToTransposonSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        serializer = QcTfToTransposonSerializer(
            data=self.qc_tf_to_transposon_data)
        assert serializer.is_valid() is True
