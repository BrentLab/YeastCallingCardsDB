import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin


class PromoterRegionsSourceFactory(BaseModelFactoryMixin,
                                   factory.django.DjangoModelFactory):
    source = 'yiming'
    providence = 'some_providence'
    notes = 'none'

    class Meta:
        model = 'callingcards.PromoterRegionsSource'
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return super()._create(model_class, *args, **kwargs)

