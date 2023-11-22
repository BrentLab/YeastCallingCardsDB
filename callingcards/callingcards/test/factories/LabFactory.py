import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin


class LabFactory(BaseModelFactoryMixin,
                 factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.Lab'

    lab = 'brent'
    notes = 'none'