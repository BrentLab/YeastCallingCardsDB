"""
UpdateModifiedMixin
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the UpdateModifiedByMixin, a custom mixin for Django Rest Framework
views to automatically update the `modifiedBy` and `modified` fields when an update operation
is performed.

Example usage:

.. code-block:: python

    from rest_framework import viewsets
    from your_app.models import YourModel
    from your_app.serializers import YourModelSerializer
    from UpdateModifiedMixin import UpdateModifiedMixin

    class YourModelViewSet(UpdateModifiedByMixin, viewsets.ModelViewSet):
        queryset = YourModel.objects.all()
        serializer_class = YourModelSerializer

This will ensure that the `modifiedBy` field is updated with the current user
and the `modified` field is updated with the current date and time whenever an update
operation is performed on a YourModel instance.
"""
from django.utils import timezone
from rest_framework import mixins


class UpdateModifiedMixin(mixins.UpdateModelMixin):    
    """
    A custom mixin to update the `modifiedBy` and `modified` fields 
    automatically when an update operation is performed.

    The `modifiedBy` field will be set to the current user 
    (from `self.request.user`) and the `modified` field will be set to the 
    current date and time.

    To use this mixin, include it in your views or viewsets that require 
    this functionality.

    Example:

    .. code-block:: python

        class YourModelViewSet(UpdateModifiedMixin, viewsets.ModelViewSet):
            queryset = YourModel.objects.all()
            serializer_class = YourModelSerializer
    """

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.modifiedBy = self.request.user
        instance.modified = timezone.now()
        instance.save()

        return super().update(request, *args, **kwargs)
    # def perform_update(self, serializer):
    #     instance = serializer.instance
    #     instance.modifiedBy = self.request.user
    #     instance.modified = timezone.now()
    #     instance.save()
    #     serializer.save()
