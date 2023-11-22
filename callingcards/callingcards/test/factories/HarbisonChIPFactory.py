import random
import factory
from ..utils import random_file_from_media_directory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory

class HarbisonChIPFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.HarbisonChIP'

    gene = factory.SubFactory(GeneFactory)
    tf = factory.SubFactory(GeneFactory)
    pval = factory.LazyFunction(lambda: round(random.random(), 3))
