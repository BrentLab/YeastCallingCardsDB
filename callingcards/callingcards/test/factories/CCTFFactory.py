import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory

class CCTFFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCTF'

    tf = factory.SubFactory(GeneFactory)
    strain = 'unknown'
    under_development = True
    notes = 'none'
