from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage
from django.db.models import FileField
import os

class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False



# credit: https://timonweb.com/django/cleanup-files-and-images-on-model-delete-in-django/
# TODO: IF THE DIRECTORY IS EMPTY, DELETE THAT, ALSO
def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """
    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None

    if field and isinstance(field, FileField):
        inst = kwargs["instance"]
        f = getattr(inst, fieldname)
        m = inst.__class__._default_manager
        if (
                hasattr(f, "path")
                and os.path.exists(f.path)
                and not m.filter(
                    **{"%s__exact" % fieldname: getattr(inst, fieldname)}
                ).exclude(pk=inst._get_pk_val())):
            try:
                default_storage.delete(f.path)
            except:
                pass
