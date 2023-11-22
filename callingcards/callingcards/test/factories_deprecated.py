import os
import random
from math import floor
import factory
from django.core.exceptions import ObjectDoesNotExist
from ..models import HopsSource, CCExperiment, BackgroundSource


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


def random_file_from_media_directory(dir_name):
    # Assuming 'factories.py' is in the root of your test
    # directory and 'data' is a subdirectory of 'test'.
    test_data_directory = os.path.join(
        os.path.dirname(__file__),
        'data',
        dir_name)

    # Ensuring the directory exists
    if not os.path.exists(test_data_directory):
        raise FileNotFoundError(
            f"Directory does not exist: {test_data_directory}")

    # List files in the specified directory within 'test/data'
    files = [f for f in os.listdir(test_data_directory)
             if os.path.isfile(os.path.join(test_data_directory, f))]

    # Return a random file path from the directory
    return os.path.join(test_data_directory, random.choice(files))


class BaseModelFactoryMixin(factory.django.DjangoModelFactory):

    uploader = factory.SubFactory(UserFactory)
    modifiedBy = factory.SelfAttribute('uploader')

    class Meta:
        abstract = True

    @factory.post_generation
    def _set_related_fields(self, create, extracted, **kwargs):
        if not create:
            # If we're not saving the instance to the database,
            # no need to set related fields
            return

        for attribute in ['uploader', 'modifiedBy']:
            value = getattr(self, attribute)
            if not value:
                value = UserFactory.create()
            setattr(self, attribute, value)
        self.save()


class BackgroundSourceFactory(BaseModelFactoryMixin,
                              factory.django.DjangoModelFactory):
    source = 'adh1'
    providence = 'some_providence'
    notes = 'none'

    class Meta:
        model = 'callingcards.BackgroundSource'

class BackgroundFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Background'

    chr = factory.SubFactory(ChrMapFactory)
    source = factory.SubFactory(BackgroundSourceFactory)
    start = 1
    end = 100
    depth = 100
    source = factory.SubFactory(BackgroundSourceFactory)


class CallingCards_s3Factory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.CallingCards_s3'

    chr_format = 'mitra'
    source = factory.SubFactory(HopsSourceFactory)
    experiment = factory.SubFactory(CCExperimentFactory)
    qbed = random_file_from_media_directory('qbed')
    notes = 'some notes'
    genomic_hops = 100
    plasmid_hops = 10

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        source = kwargs.get('source')
        if source:
            try:
                source = HopsSource.objects.get(source=source)
            except ObjectDoesNotExist:
                source = HopsSourceFactory.create(source=source)
            kwargs['source'] = source
        return super()._create(model_class, *args, **kwargs)


class CallingCardsSigFactory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):

    experiment = factory.SubFactory(CCExperimentFactory)
    hops_source = factory.SubFactory(HopsSourceFactory)
    background_source = factory.SubFactory(BackgroundSourceFactory)
    promoter_source = factory.SubFactory(PromoterRegionsSourceFactory)
    file = random_file_from_media_directory('callingcardssig')
    notes = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = 'callingcards.callingcardssig'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        hops_source = kwargs.get('hops_source')
        experiment = kwargs.get('experiment')
        background_source = kwargs.get('background_source')
        if hops_source:
            try:
                hops_source = HopsSource.objects.get(source=hops_source)
            except ObjectDoesNotExist:
                hops_source = HopsSourceFactory.create(source=hops_source)
            kwargs['hops_source'] = hops_source
        if experiment:
            try:
                experiment = CCExperiment.objects.get(experiment=experiment)
            except ObjectDoesNotExist:
                experiment = CCExperimentFactory.create(experiment=experiment)
            kwargs['experiment'] = experiment
        if background_source:
            try:
                background_source = BackgroundSource.objects.get(
                    source=background_source)
            except ObjectDoesNotExist:
                background_source = BackgroundSourceFactory.create(
                    source=background_source)
            kwargs['background_source'] = background_source

        return super()._create(model_class, *args, **kwargs)
    
    
class CCExperimentFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCExperiment'

    tf = factory.SubFactory(CCTFFactory)
    batch = factory.Sequence(lambda n: f'run_{n}')
    batch_replicate = 1
    lab = factory.SubFactory(LabFactory)

class CCTFFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCTF'

    tf = factory.SubFactory(GeneFactory)
    strain = 'unknown'
    under_development = True
    notes = 'none'

class ChipExo_s3Factory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChipExo_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    chipexo_id = 1234
    replicate = 1
    accession = 'SRR1234567'
    sra_accession = 'SRA1234567'
    condition = 'YPD'
    parent_condition = 'YPD'
    sig_count = 100
    control_count = 100
    sig_fraction = .5
    sig_ctrl_scaling = .5
    file = random_file_from_media_directory('chipexo')


class ChipExoSigFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChipExoSig'

    chipexodata_id = factory.SubFactory(ChipExo_s3Factory)
    promoterregions_id = factory.SubFactory(PromoterRegions_s3Factory)
    file = random_file_from_media_directory('chipexosig')


class ChipExoFactory(BaseModelFactoryMixin,
                     factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.ChipExo'

    gene = factory.SubFactory(GeneFactory)
    tf = factory.SubFactory(GeneFactory)
    strength = factory.LazyFunction(lambda: round(random.random(), 3))
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
    type = 'genomic'


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


class PromoterRegionsSourceFactory(BaseModelFactoryMixin,
                                   factory.django.DjangoModelFactory):
    source = 'yiming'
    providence = 'some_providence'
    notes = 'none'

    class Meta:
        model = 'callingcards.PromoterRegionsSource'


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
    # factory.Iterator(['not_orf', 'yiming'])
    source = factory.SubFactory(PromoterRegionsSourceFactory)


class PromoterRegions_s3Factory(BaseModelFactoryMixin,
                                factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.PromoterRegions_s3'

    chr_format = 'igenomes'
    source = factory.SubFactory(PromoterRegionsSourceFactory)
    file = random_file_from_media_directory('promoter_regions')


class HarbisonChIPFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.HarbisonChIP'

    gene = factory.SubFactory(GeneFactory)
    tf = factory.SubFactory(GeneFactory)
    pval = factory.LazyFunction(lambda: round(random.random(), 3))


class HarbisonChIP_s3Factory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.HarbisonChIP_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    condition = 'YPD'
    file = random_file_from_media_directory('harbisonchip')


class Hu_s3Factory(BaseModelFactoryMixin,
                   factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.Hu_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    file = random_file_from_media_directory('hu')


class KemmerenTFKO_s3Factory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.KemmerenTFKO_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    reference = 'wt'
    file = random_file_from_media_directory('chipexo')


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


class McIsaacZEV_s3Factory(BaseModelFactoryMixin,
                           factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.McIsaacZEV_s3'

    tf = factory.SubFactory(GeneFactory)
    strain = 'unknown'
    date = '2023-11-07'
    restriction = 'P'
    mechanism = 'ZEV'
    time = '0'
    file = random_file_from_media_directory('mcisaac')

class LabFactory(BaseModelFactoryMixin,
                 factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Lab'

    lab = 'brent'
    notes = 'none'

class HopsSourceFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.HopsSource'

    source = factory.Sequence(lambda n: f"source{n}")
    providence = 'some_providence'
    notes = 'none'

    @classmethod
    def get_or_create(cls, **kwargs):
        try:
            return HopsSource.objects.get(**kwargs)
        except HopsSource.DoesNotExist:
            return cls.create(**kwargs)


class HopsFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Hops'

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 100)
    end = factory.LazyAttribute(lambda o: o.start+1)
    depth = factory.Sequence(lambda n: floor(random.uniform(1, 200)))
    experiment = factory.SubFactory(CCExperimentFactory)


# class HopsReplicateSigFactory(BaseModelFactoryMixin,
#                               factory.django.DjangoModelFactory):

#     class Meta:
#         model = 'callingcards.HopsReplicateSig'

#     experiment = factory.SubFactory(CCExperimentFactory)
#     promoter = factory.SubFactory(PromoterRegionsFactory)
#     bg_hops = factory.Sequence(lambda n: floor(random.uniform(0, 200)))
#     expr_hops = factory.Sequence(lambda n: floor(random.uniform(0, 200)))
#     poisson_pval = factory.Sequence(lambda n: round(random.uniform(0, 1), 5))
#     hypergeom_pval = factory.LazyAttribute(lambda o:
#           close_value(o.poisson_pval))
#     background = factory.Iterator(['adh1'])

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


class RegulatorFactory(BaseModelFactoryMixin,
                       factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Regulator'

    regulator = factory.SubFactory(GeneFactory)
    notes = 'none'
