import factory
from django.core.exceptions import ObjectDoesNotExist
from ..utils import random_file_from_media_directory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .PromoterRegionsSourceFactory import PromoterRegionsSourceFactory
from .ChrMapFactory import ChrMapFactory
from ...models import PromoterRegionsSource


class PromoterRegions_s3Factory(BaseModelFactoryMixin,
                                factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.PromoterRegions_s3'

    chr_format = 'numbered'
    source = factory.SubFactory(PromoterRegionsSourceFactory)
    file = random_file_from_media_directory('promoter_regions')

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        source = kwargs.get('source')
        ChrMapFactory.create()
        try:
            source = PromoterRegionsSourceFactory.create(pk=source.pk)
        except ObjectDoesNotExist:
            source = PromoterRegionsSourceFactory.create()
        kwargs['source'] = source.pk
        return super()._build(model_class, *args, **kwargs)