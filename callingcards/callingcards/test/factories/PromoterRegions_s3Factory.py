import factory
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import random_file_from_media_directory, get_file_content
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .PromoterRegionsSourceFactory import PromoterRegionsSourceFactory
from .ChrMapFactory import ChrMapFactory


class PromoterRegions_s3Factory(BaseModelFactoryMixin,
                                factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.PromoterRegions_s3'

    chr_format = 'numbered'
    source = factory.SubFactory(PromoterRegionsSourceFactory)
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test_promoter_regions.bed.gz',
            content=get_file_content(random_file_from_media_directory('promoter_regions')), # noqa
            content_type='application/gzip'
        )
    )

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