import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import random_file_from_media_directory, get_file_content
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
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test_chipexo.csv.gz',
            content=get_file_content(random_file_from_media_directory('chipexo')),  # noqa
            content_type='application/gzip'
        )
    )

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        regulator = RegulatorFactory.create()
        kwargs['regulator'] = regulator.pk

        return super()._build(model_class, *args, **kwargs)
