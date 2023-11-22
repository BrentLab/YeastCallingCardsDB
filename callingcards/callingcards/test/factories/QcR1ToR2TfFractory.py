import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .CCExperimentFactory import CCExperimentFactory


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