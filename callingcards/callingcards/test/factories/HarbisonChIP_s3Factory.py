import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from ..utils import random_file_from_media_directory, get_file_content
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .RegulatorFactory import RegulatorFactory
from ...models import Regulator


class HarbisonChIP_s3Factory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.HarbisonChIP_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    condition = 'YPD'
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test_harbison.csv.gz',
            content=get_file_content(random_file_from_media_directory('harbisonchip')),  # noqa
            content_type='application/gzip'
        )
    )

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        regulator = kwargs.get('regulator')
        try:
            regulator = Regulator.objects.get(pk=regulator.pk)
        except ObjectDoesNotExist:
            regulator = RegulatorFactory.create(pk=regulator.pk)
        kwargs['regulator'] = regulator.pk
        return super()._build(model_class, *args, **kwargs)

