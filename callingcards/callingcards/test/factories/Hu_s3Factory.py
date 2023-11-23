import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from ..utils import random_file_from_media_directory, get_file_content
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .RegulatorFactory import RegulatorFactory
from ...models import Regulator


class Hu_s3Factory(BaseModelFactoryMixin,
                   factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.Hu_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test_harbison.csv.gz',
            content=get_file_content(random_file_from_media_directory('hu')),  # noqa
            content_type='application/gzip'
        )
    )

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        regulator = kwargs.get('regulator')
        try:
            regulator = Regulator.objects.get(pk=regulator.pk)
        except ObjectDoesNotExist:
            regulator = RegulatorFactory.create()
        kwargs['regulator'] = regulator.pk
        return super()._build(model_class, *args, **kwargs)

