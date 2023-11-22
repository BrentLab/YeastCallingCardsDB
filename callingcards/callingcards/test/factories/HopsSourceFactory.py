import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin


class HopsSourceFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.HopsSource'
        django_get_or_create = ('source',)

    source = factory.Sequence(lambda n: f"source{n}")
    providence = 'some_providence'
    notes = 'none'
