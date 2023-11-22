import factory
from callingcards.users.test.factories import UserFactory


class BaseModelFactoryMixin(factory.django.DjangoModelFactory):

    uploader = factory.SubFactory(UserFactory)
    modifiedBy = factory.SelfAttribute('uploader')

    class Meta:
        abstract = True

    @factory.post_generation
    def _set_related_fields(self, create, extracted, **kwargs):
        if not create:
            # If we're not saving the instance to the database,
            # no need to set related fields
            return

        for attribute in ['uploader', 'modifiedBy']:
            value = getattr(self, attribute)
            if not value:
                value = UserFactory.create()
            setattr(self, attribute, value)
        self.save()