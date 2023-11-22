import random
import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory


class ChipExoFactory(BaseModelFactoryMixin,
                     factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.ChipExo'

    gene = factory.SubFactory(GeneFactory)
    tf = factory.SubFactory(GeneFactory)
    strength = factory.LazyFunction(lambda: round(random.random(), 3))
