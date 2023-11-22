import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .CCExperimentFactory import CCExperimentFactory


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
