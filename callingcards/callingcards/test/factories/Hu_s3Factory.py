import factory
from ..utils import random_file_from_media_directory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .RegulatorFactory import RegulatorFactory


class Hu_s3Factory(BaseModelFactoryMixin,
                   factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.Hu_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    file = random_file_from_media_directory('hu')

