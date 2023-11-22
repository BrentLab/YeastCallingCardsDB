import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .CCExperimentFactory import CCExperimentFactory


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
