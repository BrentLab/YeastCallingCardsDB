"""
.. module:: base_model
   :synopsis: Module for the BaseModel class.

This module provides an abstract base class for models, defining common fields
for tracking the user who uploaded the data, the date of uploading, and the
last modification date and user who made the modification. It is intended to be
used as a base class for other models to inherit from.

.. author:: Chase Mateusiak
.. date:: 2023-04-17
"""
from uuid import UUID
from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.conf import settings  # pylint: disable=import-error # noqa # type: ignore


class BaseModel(models.Model):
    """
    An abstract base model that includes common fields for tracking the user
    who uploaded the data, the date of uploading, and the last modification
    date and user who made the modification.

    Inherit from this class to provide these common fields for other models.

    :ivar uploader: ForeignKey to the user model, representing the user who
        uploaded the data.
    :ivar uploadDate: DateField, automatically set to the date the object was
        created.
    :ivar modified: DateTimeField, automatically set to the current date and 
        time when the object is updated. Note that this field is only 
        updated when the object is saved using the save() method, not when 
        using queryset.update().
    :ivar modifiedBy: ForeignKey to the user model, representing the user who
        last modified the data.

    Example usage::

        from django.db import models
        from .base_model import BaseModel

        class MyModel(BaseModel):
            field1 = models.CharField(max_length=100)
            field2 = models.IntegerField()
    """
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_uploader')
    uploadDate = models.DateField(auto_now_add=True)
    # record when the record is modified
    # note: this only updates with model.save(), not queryset.update
    #       see docs -- may need to write some code to update this field
    #       for update statement when only certain fields are changed?
    modified = models.DateTimeField(auto_now=True)
    modifiedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_modifiedBy')

    class Meta:
        abstract = True
