import factory
from ..utils import random_file_from_media_directory
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
    file = random_file_from_media_directory('mcisaac')
