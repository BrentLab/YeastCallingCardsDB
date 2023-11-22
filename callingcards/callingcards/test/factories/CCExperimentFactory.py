import factory
from .BaseModelFactoryMixin import BaseModelFactoryMixin
from .CCTFFactory import CCTFFactory
from .LabFactory import LabFactory


class CCExperimentFactory(BaseModelFactoryMixin,
                          factory.django.DjangoModelFactory):

    class Meta:
        model = 'callingcards.CCExperiment'
        django_get_or_create = ('tf', 'lab')

    tf = factory.SubFactory(CCTFFactory)
    batch = factory.Sequence(lambda n: f'run_{n}')
    batch_replicate = 1
    lab = factory.SubFactory(LabFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        tf = kwargs.get('tf')
        if not tf.pk:
            tf = CCTFFactory.create()
            kwargs['tf'] = tf
        lab = kwargs.get('lab')
        if not lab.pk:
            lab = LabFactory.create()
            kwargs['lab'] = lab
        return super()._create(model_class, *args, **kwargs)
