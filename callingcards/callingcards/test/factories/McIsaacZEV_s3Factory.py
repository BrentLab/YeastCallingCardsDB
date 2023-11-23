import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import random_file_from_media_directory, get_file_content
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .GeneFactory import GeneFactory


class McIsaacZEV_s3Factory(BaseModelFactoryMixin,
                           factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.McIsaacZEV_s3'

    tf = factory.SubFactory(GeneFactory)
    strain = 'unknown'
    date = '2023-11-07'
    restriction = 'P'
    mechanism = 'ZEV'
    time = '0'
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test_mcisaac.csv.gz',
            content=get_file_content(random_file_from_media_directory('mcisaac')), # noqa
            content_type='application/gzip'
        )
    )
