import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .ChrMapFactory import ChrMapFactory


class GeneFactory(BaseModelFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Gene'
        skip_postgeneration_save = True

    chr = factory.SubFactory(ChrMapFactory)
    start = factory.Sequence(lambda n: n * 100)
    end = factory.Sequence(lambda n: n * 100 + 50)
    strand = factory.Iterator(['+', '-', '*'])
    type = 'unknown'
    gene_biotype = 'unknown'
    locus_tag = factory.Sequence(lambda n: f'unknown_{n}')
    gene = factory.Sequence(lambda n: f'unknown_{n}')
    source = 'source'
    alias = factory.Sequence(lambda n: f'unknown_{n}')
    note = 'none'

