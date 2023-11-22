import factory
from django.core.exceptions import ObjectDoesNotExist
from ...models import Regulator
from ..utils import random_file_from_media_directory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .RegulatorFactory import RegulatorFactory


class ChipExo_s3Factory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChipExo_s3'

    regulator = factory.SubFactory(RegulatorFactory)
    chipexo_id = 1234
    replicate = 1
    accession = 'SRR1234567'
    sra_accession = 'SRA1234567'
    condition = 'YPD'
    parent_condition = 'YPD'
    sig_count = 100
    control_count = 100
    sig_fraction = .5
    sig_ctrl_scaling = .5
    file = random_file_from_media_directory('chipexo')
 
    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        regulator = RegulatorFactory.create()
        kwargs['regulator'] = regulator.pk

        return super()._build(model_class, *args, **kwargs)

