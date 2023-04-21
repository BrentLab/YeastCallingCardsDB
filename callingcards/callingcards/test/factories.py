import random
from math import floor
import factory
import uuid


from callingcards.users.test.factories import UserFactory


def close_value(value, min_diff=0.0001, max_diff=0.01):
    """
    Generate a value close to the input value within a specified range.

    Args:
        value (float): The input value to generate a close value for.
        min_diff (float, optional): The minimum difference between the
          input value and the generated value. Defaults to 0.0001.
        max_diff (float, optional): The maximum difference between the
          input value and the generated value. Defaults to 0.01.

    Returns:
        float: A value within the specified range of the input value.
    """
    # Generate a random difference within the range [min_diff, max_diff]
    diff = random.uniform(min_diff, max_diff)

    # Randomly choose the sign of the difference (-1 or 1)
    sign = random.choice([-1, 1])

    # Calculate and return the new value within the specified range of the
    # input value
    return round(value + sign * diff, 5)


class BaseModelFactoryMixin(factory.django.DjangoModelFactory):

    uploader = factory.SubFactory(UserFactory)
    modifiedBy = factory.SelfAttribute('uploader')

    class Meta:
        abstract = True

    @factory.post_generation
    def _set_related_fields(self, create, extracted, **kwargs):
        if not create:
            # If we're not saving the instance to the database, no need to set related fields
            return

        for attribute in ['uploader', 'modifiedBy']:
            value = getattr(self, attribute)
            if not value:
                value = UserFactory.create()
            setattr(self, attribute, value)
        self.save()


class ChrMapFactory(BaseModelFactoryMixin,
                    factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChrMap'

    refseq = 'NC_001133.9'
    igenomes = 'I'
    ensembl = 'I'
    ucsc = 'chrI'
    mitra = 'NC_001133'
    numbered = 1
    chr = 'chr1'
    seqlength = 230218


class GeneFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Gene'
        django_get_or_create = ('locus_tag',)

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 100)
    end = factory.Sequence(lambda n: n * 100 + 50)
    strand = factory.Iterator(['+', '-', '*'])
    type = 'unknown'
    gene_biotype = 'unknown'
    locus_tag = factory.Sequence(lambda n: f'unknown_{n}')
    gene = factory.Sequence(lambda n: f'unknown_{n}')
    source = 'source'
    alias = factory.Sequence(lambda n: f'unknown_{n}')
    note = 'none'

class PromoterRegionsFactory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.PromoterRegions'

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 200)
    end = factory.Sequence(lambda n: n * 200 + 100)
    strand = factory.Iterator(['+', '-', '*'])
    associated_feature = factory.SubFactory(GeneFactory)
    score = 100
    source = factory.Iterator(['not_orf', 'yiming'])

class HarbisonChIPFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.HarbisonChIP'

    gene = factory.SubFactory(GeneFactory)
    tf = factory.SubFactory(GeneFactory)
    pval = factory.LazyFunction(lambda: round(random.random(), 3))


class KemmerenTFKOFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.KemmerenTFKO'

    gene = factory.SubFactory(GeneFactory)
    effect = factory.LazyFunction(lambda: round(random.uniform(-10, 10), 2))
    padj = factory.LazyFunction(lambda: round(random.random(), 3))
    tf = factory.SubFactory(GeneFactory)


class McIsaacZEVFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.McIsaacZEV'

    gene = factory.SubFactory(GeneFactory)
    effect = factory.LazyFunction(lambda: round(random.uniform(-5, 5), 2))
    tf = factory.SubFactory(GeneFactory)

class BackgroundFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Background'

    chr = factory.SubFactory(ChrMapFactory)
    start = 1
    end = 100
    depth = 100
    source = 'adh1'

class CCTFFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCTF'

    tf = factory.SubFactory(GeneFactory)
    strain = 'unknown'
    under_development = True
    notes = 'none'

class CCExperimentFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCExperiment'

    tf = factory.SubFactory(CCTFFactory)
    batch = 'run_1234'
    batch_replicate = 1

class HopsFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Hops'

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 100)
    end = factory.LazyAttribute(lambda o: o.start+1)
    depth = factory.Sequence(lambda n: floor(random.uniform(1, 200)))
    experiment = factory.SubFactory(CCExperimentFactory)

class HopsReplicateSigFactory(BaseModelFactoryMixin,
                              factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.HopsReplicateSig'

    experiment = factory.SubFactory(CCExperimentFactory)
    promoter = factory.SubFactory(PromoterRegionsFactory)
    bg_hops = factory.Sequence(lambda n: floor(random.uniform(0, 200)))
    expr_hops = factory.Sequence(lambda n: floor(random.uniform(0, 200)))
    poisson_pval = factory.Sequence(lambda n: round(random.uniform(0, 1), 5))
    hypergeom_pval = factory.LazyAttribute(lambda o: close_value(o.poisson_pval))
    background = factory.Iterator(['adh1'])

class QcMetricsFactory(BaseModelFactoryMixin,
                       factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcMetrics'

    # uploader = factory.SubFactory(UserFactory)
    # uploadDate = factory.Faker('date_time')
    # modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    total_reads = 3e6
    unmapped = 3e6
    multimapped = 3e6
    genome_mapped = 3e6
    plasmid_mapped = 3e6
    hpaii = 3e6
    hinp1i = 3e6
    taqai = 3e6
    undet = 3e6
    note = 'some notes'

class QcManualReviewFactory(BaseModelFactoryMixin,
                            factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcManualReview'

    experiment = factory.SubFactory(CCExperimentFactory)
    rank_recall = 'unreviewed'
    chip_better = 'yes'
    data_usable = 'no'
    passing_replicate = 'unreviewed'
    note = 'arrrr mate-y harrrr be sea monsters!'

class QcR1ToR2TfFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcR1ToR2Tf'

    # uploader = factory.SubFactory(UserFactory)
    # uploadDate = factory.Faker('date_time')
    # modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    edit_dist = 0
    tally = 4
    note = 'some notes'

class QcR2ToR1TfFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcR2ToR1Tf'

    # uploader = factory.SubFactory(UserFactory)
    # uploadDate = factory.Faker('date_time')
    # modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    edit_dist = 0
    tally = 4
    note = 'some notes'


class QcTfToTransposonFactory(BaseModelFactoryMixin,
                              factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.QcTfToTransposon'

    # uploader = factory.SubFactory(UserFactory)
    # uploadDate = factory.Faker('date_time')
    # modified = factory.Faker('date_time')
    experiment = factory.SubFactory(CCExperimentFactory)
    edit_dist = 0
    tally = 4
    note = 'some notes'
