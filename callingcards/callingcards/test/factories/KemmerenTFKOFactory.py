import random
import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory


class KemmerenTFKOFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.KemmerenTFKO'

    gene = factory.SubFactory(GeneFactory)
    effect = factory.LazyFunction(lambda: round(random.uniform(-10, 10), 2))
    padj = factory.LazyFunction(lambda: round(random.random(), 3))
    tf = factory.SubFactory(GeneFactory)
