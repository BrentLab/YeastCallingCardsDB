from django.utils import timezone

class UpdateModifiedSerializerMixin:
    """
    A custom serializer mixin to update the `modified_by_field` and 
    `modified_field` automatically when an update operation is performed.

    The `modified_by_field` will be set to the current user 
    (from `self.context['request'].user`) and the `modified_field` will be set 
    to the current date and time.

    To use this mixin, include it in your serializers that require this 
    functionality and set the class attributes `modified_by_field` and 
    `modified_field` accordingly.

    Example:

    .. code-block:: python

        class YourModelSerializer(UpdateModifiedSerializerMixin,
                                  serializers.ModelSerializer):
            modified_by_field = 'modifiedBy'
            modified_field = 'modified'

            class Meta:
                model = YourModel
                fields = '__all__'
    """

    modified_by_field = 'modifiedBy'
    modified_field = 'modified'

    def update(self, instance, validated_data):
        user = self.context['request'].user
        setattr(instance, self.modified_by_field, user)
        setattr(instance, self.modified_field, timezone.now())
        return super().update(instance, validated_data)
    