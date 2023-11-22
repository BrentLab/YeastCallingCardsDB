import logging
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class FileUploadMixin:
    """
    A mixin for models that have a file field that should be uploaded to a
    specific directory and renamed based on the instance's ID. This mixin
    requires that the model have a FileField with an `upload_to` argument

    Example usage:

    .. code-block:: python

        class Hu_s3(BaseModel, FileUploadMixin):
        # Temporary upload path
        file = models.FileField(upload_to='temp', help_text="A gziped csv...")

        def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            self.update_file_name('file', 'hu', 'tsv.gz')
            super().save(update_fields=['file'])

        # Other fields and methods...

    """

    def update_file_name(self,
                         file_field_name: str,
                         upload_dir: str,
                         extension: str) -> None:
        """
        A utility method to update the file name based on the instance's ID.
        This method should be called in the `save` method of the model.

        :param file_field_name: The name of the file field to update.
        :type file_field_name: str
        :param upload_dir: The directory to upload the file to.
        :type upload_dir: str
        :param extension: The file extension to use.
        :type extension: str

        :return: None
        :rtype: None
        """
        logger.debug('Updating file name for %s to '
                     '%s/%s.%s', self, upload_dir, self.pk, extension)
        file_field = getattr(self, file_field_name, None)
        if file_field and self.pk and file_field.name:
            # Define new filename with ID
            new_filename = f'{upload_dir}/{self.pk}.{extension}'

            # Move and rename the file if it exists
            if default_storage.exists(file_field.name):
                default_storage.save(new_filename, file_field)
                default_storage.delete(file_field.name)

            # Update the file field to new path
            file_field.name = new_filename
            setattr(self, file_field_name, file_field)
