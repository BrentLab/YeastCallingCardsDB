import factory
from django.core.exceptions import ObjectDoesNotExist
from ..utils import random_file_from_media_directory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .CCExperimentFactory import CCExperimentFactory
from .HopsSourceFactory import HopsSourceFactory
from .BackgroundSourceFactory import BackgroundSourceFactory
from .PromoterRegionsSourceFactory import PromoterRegionsSourceFactory
from ...models import (HopsSource, CCExperiment,
                       BackgroundSource, PromoterRegionsSource)


class CallingCardsSigFactory(BaseModelFactoryMixin,
                             factory.django.DjangoModelFactory):

    experiment = factory.SubFactory(CCExperimentFactory)
    hops_source = factory.SubFactory(HopsSourceFactory)
    background_source = factory.SubFactory(BackgroundSourceFactory)
    promoter_source = factory.SubFactory(PromoterRegionsSourceFactory)
    file = random_file_from_media_directory('callingcardssig')
    notes = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = 'callingcards.callingcardssig'

    @classmethod
    def _build(cls, model_class, *args, **kwargs):

        hops_source = kwargs.get('hops_source')
        try:
            hops_source = HopsSource.objects.get(source=hops_source.pk)
        except ObjectDoesNotExist:
            hops_source = HopsSourceFactory.create(source=hops_source.pk)
        kwargs['hops_source'] = hops_source.pk

        experiment = kwargs.get('experiment')
        try:
            experiment = CCExperiment.objects.get(pk=experiment.pk)
        except ObjectDoesNotExist:
            experiment = CCExperimentFactory.create(pk=experiment.pk)
        kwargs['experiment'] = experiment.pk

        background_source = kwargs.get('background_source')
        try:
            background_source = BackgroundSource.objects\
                .get(source=background_source.pk)
        except ObjectDoesNotExist:
            background_source = BackgroundSourceFactory\
                .create(pk=background_source.pk)
        kwargs['background_source'] = background_source.pk

        promoter_source = kwargs.get('promoter_source')
        try:
            promoter_source = PromoterRegionsSource.objects\
                .get(source=promoter_source.pk)
        except ObjectDoesNotExist:
            promoter_source = PromoterRegionsSourceFactory\
                .create(pk=promoter_source.pk)
        kwargs['promoter_source'] = promoter_source.pk

        return super()._build(model_class, *args, **kwargs)
