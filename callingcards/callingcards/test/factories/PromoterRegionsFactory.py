import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .ChrMapFactory import ChrMapFactory
from .GeneFactory import GeneFactory
from .PromoterRegionsSourceFactory import PromoterRegionsSourceFactory



class PromoterRegionsFactory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.PromoterRegions'

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 200)
    end = factory.Sequence(lambda n: n * 200 + 100)
    strand = factory.Iterator(['+', '-', '*'])
    associated_feature = factory.SubFactory(GeneFactory)
    score = 100
    # factory.Iterator(['not_orf', 'yiming'])
    source = factory.SubFactory(PromoterRegionsSourceFactory)

