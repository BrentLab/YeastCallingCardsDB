import random
import factory
from math import floor
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .ChrMapFactory import ChrMapFactory
from .CCExperimentFactory import CCExperimentFactory


class HopsFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Hops'

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 100)
    end = factory.LazyAttribute(lambda o: o.start+1)
    depth = factory.Sequence(lambda n: floor(random.uniform(1, 200)))
    experiment = factory.SubFactory(CCExperimentFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        chr_record = kwargs.get('chr')
        if not chr_record.pk:
            chr_record = ChrMapFactory.create()
            kwargs['chr'] = chr_record
        return super()._create(model_class, *args, **kwargs)

