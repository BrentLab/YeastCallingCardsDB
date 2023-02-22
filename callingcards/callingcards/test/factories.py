import factory

from callingcards.users.test.factories import UserFactory
from ..models import *  # pylint: disable=W0401,W0614 # noqa

__all__ = ['ChrMapFactory', 'GeneFactory', 'PromoterRegionsFactory',
           'HarbisonChIPFactory', 'KemmerenTFKOFactory',
           'BackgroundFactory', 'CCTFFactory',
           'CCExperimentFactory', 'HopsFactory',
           'HopsReplicateSigFactory', 'QcMetricsFactory',
           'QcManualReviewFactory', 'QcR1ToR2TfFactory',
           'QcR2ToR1TfFactory', 'QcTfToTransposonFactory']

class ChrMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChrMap'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    refseq = 'NC_001133.9'
    igenomes = 'I'
    ensembl = 'I'
    ucsc = 'chrI'
    mitra = 'NC_001133'
    numbered = 1
    chr = 'chr1'
    seqlength = 230218


class GeneFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Gene'
        django_get_or_create = ('systematic',)

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    chr = factory.SubFactory(ChrMapFactory)
    start = 100
    end = 200
    strand = '+'
    feature_ontology = 'gene'
    biotype = 'protein_coding'
    systematic = factory.Faker('pystr', min_chars=10, max_chars=15)
    name = factory.Faker('pystr', min_chars=10, max_chars=15)
    source = 'ensembl'
    alias = factory.Faker('pystr', min_chars=10, max_chars=15)
    tf = True

class PromoterRegionsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.PromoterRegions'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    chr = factory.SubFactory(ChrMapFactory)
    start = 1
    end = 100
    strand = '+'
    associated_feature = factory.SubFactory(GeneFactory)
    score = 100.0
    source = 'yiming'

class HarbisonChIPFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.HarbisonChIP'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    gene = factory.SubFactory(GeneFactory)
    effect = 3.5
    pval = 0.0001
    tf = factory.SubFactory(GeneFactory)

class KemmerenTFKOFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.KemmerenTFKO'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    gene = factory.SubFactory(GeneFactory)
    effect = 3.5
    padj = 0.05
    tf = factory.SubFactory(GeneFactory)


class BackgroundFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Background'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    chr = factory.SubFactory(ChrMapFactory)
    start = 1
    end = 100
    depth = 100
    source = 'adh1'

class CCTFFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCTF'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    tf = factory.SubFactory(GeneFactory)
    strain = 'some_strain'
    under_development = True
    notes = 'some notes'

class CCExperimentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCExperiment'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    tf = factory.SubFactory(CCTFFactory)
    batch = 'run_1234'
    batch_replicate = 1

class HopsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Hops'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    chr = factory.SubFactory(ChrMapFactory)
    start = 1
    end = 100
    depth = 200
    experiment = factory.SubFactory(CCExperimentFactory)

class HopsReplicateSigFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.HopsReplicateSig'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    chr = factory.SubFactory(ChrMapFactory)
    start = 1
    end = 100
    bg_hops = 100
    expr_hops = 200
    poisson_pval = 0.0001
    hypergeom_pval = 0.0001
    background = 'adh1'
    promoters = 'yiming'

class QcMetricsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcMetrics'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    total_aligned = 3e6
    unmapped = 3e6
    multimapped = 3e6
    genome_mapped = 3e6
    plasmid_mapped = 3e6
    # note the sum of the hops is total hops
    genome_hops = 3e6
    plasmid_hops = 3e6
    hpaii = 3e6
    hinp1i = 3e6
    taqai = 3e6
    undet = 3e6

class QcManualReviewFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcManualReview'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    rank_recall = 'unreviewed'
    chip_better = 'yes'
    data_usable = 'no'
    passing_replicate = 'unreviewed'
    notes = 'arrrr mate-y harrrr be sea monsters!'

class QcR1ToR2TfFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcR1ToR2Tf'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    edit_dist = 0
    tally = 4

class QcR2ToR1TfFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcR2ToR1Tf'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    edit_dist = 0
    tally = 4

class QcTfToTransposonFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcTfToTransposon'

    uploader = factory.SubFactory(UserFactory)
    uploadDate = factory.Faker('date_time')
    modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    edit_dist = 0
    tally = 4
