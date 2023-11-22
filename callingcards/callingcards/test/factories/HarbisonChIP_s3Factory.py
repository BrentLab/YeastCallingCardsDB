import factory
from ..utils import random_file_from_media_directory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .RegulatorFactory import RegulatorFactory


class HarbisonChIP_s3Factory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.HarbisonChIP_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    condition = 'YPD'
    file = random_file_from_media_directory('harbisonchip')

