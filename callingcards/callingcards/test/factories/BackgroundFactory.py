import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .BackgroundSourceFactory import BackgroundSourceFactory
from .ChrMapFactory import ChrMapFactory


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

