import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from ...models import BackgroundSource


class BackgroundSourceFactory(BaseModelFactoryMixin,
                              factory.django.DjangoModelFactory):
    source = 'adh1'
    providence = 'some_providence'
    notes = 'none'

    class Meta:
        model = 'callingcards.BackgroundSource'
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return super()._create(model_class, *args, **kwargs)
