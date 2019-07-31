from django.core.files.storage import get_storage_class
from storages.backends.gcloud import GoogleCloudStorage, GoogleCloudFile
from google.api_core.exceptions import NotFound
import logging

from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible
from django.conf import settings
from storages.utils import safe_join


class GoogleCloudStorageMixin(GoogleCloudStorage):
    """
    GCP storage mixin to add location prefix for each file.
    """

    def _normalize_name(self, name):
        name = super(GoogleCloudStorageMixin, self)._normalize_name(name)
        return name


class GCPStaticStorage(GoogleCloudStorageMixin):
    """
    GCP storage backend that saves the files locally, too.
    """
    bucket_name = settings.GCP_STATIC_BUCKET
    location = settings.GCP_STATIC_LOCATION
    cache_control = "max-age=86400"

    def __init__(self, **settings):
        super(GCPStaticStorage, self).__init__(**settings)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def url(self, name):
        return settings.STATIC_URL + name

    def save(self, name, content, max_length=None):
        self.local_storage._save(name, content)
        super(GCPStaticStorage, self).save(name, self.local_storage._open(name))
        return name


@deconstructible
class GCPMediaStorage(GoogleCloudStorageMixin):
    """
    GCP storage backend for public media
    """
    bucket_name = settings.GS_BUCKET_NAME
    location = settings.GCP_MEDIA_LOCATION
    cache_control = "max-age=86400"

    def url(self, name):
        return settings.MEDIA_URL + name


@deconstructible
class GCPPrivateMediaStorage(GoogleCloudStorage):
    bucket_name = settings.GCP_PRIVATE_MEDIA_BUCKET
    cache_control = "private, max-age=3600"

    def _open(self, name, mode='rb'):
        # name = self._normalize_name(clean_name(name))
        file_object = GoogleCloudFile(name, mode, self)
        if not file_object.blob:
            raise IOError(u'File does not exist: %s' % name)
        return file_object

    def _save(self, name, content):
        content.name = name
        file = GoogleCloudFile(name, 'rw', self)
        file.blob.upload_from_file(
            content, size=content.size,
            content_type=file.mime_type)
        return name

    def exists(self, name):
        if not name:
            try:
                self.bucket
                return True
            except ImproperlyConfigured:
                return False
        return bool(self.bucket.get_blob(name))


@deconstructible
class GCPInvoiceStorage(GCPPrivateMediaStorage):
    bucket_name = settings.GCP_INVOICE_BUCKET
    cache_control = "no-store"


@deconstructible
class GCPResumeBuilderStorage(GCPPrivateMediaStorage):
    bucket_name = settings.GCP_RESUME_BUILDER_BUCKET
    cache_control = "no-store"
