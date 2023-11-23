import factory
from django.core.exceptions import ObjectDoesNotExist
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory
from ...models import Gene


class RegulatorFactory(BaseModelFactoryMixin,
                       factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Regulator'
        django_get_or_create = ('regulator',)
        skip_postgeneration_save = True

    regulator = factory.SubFactory(GeneFactory)
    notes = 'none'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        regulator = kwargs.get('regulator')
        try:
            regulator = Gene.objects.get(pk=regulator.pk)
        except ObjectDoesNotExist:
            regulator = GeneFactory.create(pk=regulator.pk)
        kwargs['regulator'] = regulator
        return super()._create(model_class, *args, **kwargs)
    
    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        regulator = GeneFactory.create()
        kwargs['regulator'] = regulator
        return super()._build(model_class, *args, **kwargs)