import random
import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory


class McIsaacZEVFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.McIsaacZEV'

    gene = factory.SubFactory(GeneFactory)
    effect = factory.LazyFunction(lambda: round(random.uniform(-5, 5), 2))
    tf = factory.SubFactory(GeneFactory)
