import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import random_file_from_media_directory, get_file_content
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .ChipExo_s3Factory import ChipExo_s3Factory
from .PromoterRegions_s3Factory import PromoterRegions_s3Factory


class ChipExoSigFactory(BaseModelFactoryMixin,
                        factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChipExoSig'

    chipexodata_id = factory.SubFactory(ChipExo_s3Factory)
    promoterregions_id = factory.SubFactory(PromoterRegions_s3Factory)
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name='test_chipexo.tsv.gz',
            content=get_file_content(random_file_from_media_directory('chipexosig')),  # noqa
            content_type='application/gzip'
        )
    )

