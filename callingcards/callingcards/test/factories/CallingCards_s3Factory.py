import factory
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import random_file_from_media_directory, get_file_content
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .HopsSourceFactory import HopsSourceFactory
from .CCExperimentFactory import CCExperimentFactory
from ...models import HopsSource


class CallingCards_s3Factory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.CallingCards_s3'

    chr_format = 'mitra'
    source = factory.SubFactory(HopsSourceFactory)
    experiment = factory.SubFactory(CCExperimentFactory)
    qbed = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test.qbed.gz',
            content=get_file_content(random_file_from_media_directory('qbed')),  # noqa
            content_type='application/gzip'
        )
    )
    notes = 'some notes'
    genomic_hops = 100
    plasmid_hops = 10

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        source = kwargs.get('source')
        if source:
            try:
                source = HopsSource.objects.get(source=source)
            except ObjectDoesNotExist:
                source = HopsSourceFactory.create(source=source)
            kwargs['source'] = source
        return super()._create(model_class, *args, **kwargs)

