import os
import random
from math import floor
import factory
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from ..models import HopsSource, Lab


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


def random_file_from_media_directory(dir):
    media_directory = default_storage.location
    files = [f for f in default_storage.listdir(dir)[1]
             if default_storage.exists(dir+'/'+f)]
    return os.path.join(dir, random.choice(files))


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


class CCTFFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCTF'

    tf = factory.SubFactory(GeneFactory)
    strain = 'unknown'
    under_development = True
    notes = 'none'


class LabFactory(BaseModelFactoryMixin,
                 factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Lab'

    lab = 'brent'
    notes = 'none'


class CCExperimentFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCExperiment'

    tf = factory.SubFactory(CCTFFactory)
    batch = factory.Sequence(lambda n: f'run_{n}')
    batch_replicate = 1
    lab = factory.SubFactory(LabFactory)


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


class Hops_s3Factory(BaseModelFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.Hops_s3'

    chr_format = 'mitra'
    source = factory.SubFactory(HopsSourceFactory)
    experiment = factory.SubFactory(CCExperimentFactory)
    qbed = random_file_from_media_directory('qbed')
    notes = 'some notes'

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


class CallingCardsSigFactory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):

    experiment = factory.SubFactory(CCExperimentFactory)
    background_source = factory.SubFactory(BackgroundSourceFactory)
    promoter_source = factory.SubFactory(PromoterRegionsSourceFactory)
    file = factory.django.FileField(
        from_path=os.path.join(
            'media',
            'analysis',
            'run_5690',
            'ccexperiment_75_yiming.csv.gz'))
    notes = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = 'callingcards.callingcardssig'
