
import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin


class ChrMapFactory(BaseModelFactoryMixin,
                    factory.django.DjangoModelFactory):
    class Meta:
        model = 'callingcards.ChrMap'
        skip_postgeneration_save = True

    refseq = 'NC_001133.9'
    igenomes = 'I'
    ensembl = 'I'
    ucsc = 'chrI'
    mitra = 'NC_001133'
    numbered = 1
    chr = 'chr1'
    seqlength = 230218
    type = 'genomic'
