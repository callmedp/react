import os
from urllib import parse
from django.core.files.storage import get_storage_class
from storages.backends.gcloud import GoogleCloudStorage, GoogleCloudFile

from google.cloud import storage

from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible
from django.conf import settings


class GCPStaticStorage(GoogleCloudStorage):
    """
    GCP storage backend that saves the files locally, too.
    """
    bucket_name = settings.GCP_STATIC_BUCKET

    def __init__(self, **settings):
        super(GCPStaticStorage, self).__init__(**settings)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def url(self, name):
        temp_url = super(GCPStaticStorage, self).url(name)
        temp_url_parsed = parse.urlparse(temp_url)
        base_url_parsed = parse.urlparse(self.local_storage.base_url)
        temp_url_parsed = temp_url_parsed._replace(scheme=base_url_parsed.scheme)
        temp_url_parsed = temp_url_parsed._replace(netloc=base_url_parsed.netloc)
        temp_url_parsed_path = list(os.path.split(temp_url_parsed.path))
        temp_url_parsed_path = os.path.join(*[
            path_component if path_component != '/' + self.bucket_name else '/' for
            path_component in temp_url_parsed_path])
        temp_url_parsed = temp_url_parsed._replace(path=temp_url_parsed_path)
        public_url = parse.urlunparse(temp_url_parsed)
        return public_url
        # return settings.STATIC_URL + name

    def save(self, name, content, max_length=None):
        self.local_storage._save(name, content)
        super(GCPStaticStorage, self).save(name, self.local_storage._open(name))
        return name


@deconstructible
class GCPPrivateMediaStorage(GoogleCloudStorage):
    bucket_name = settings.GCP_PRIVATE_MEDIA_BUCKET

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

#
# class GoogleCloudMediaUploader(object):
#
#     BASE_UPLOAD_PATH = settings.GCP_UPLOADS_DIR
#
#     def __init__(self, file, base_upload_path=None):
#         # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.GCP_SECRET_FILE
#         self.storage_client = storage.Client()
#         # self.bucket = self.storage_client.bucket(settings.GCP_PRIVATE_MEDIA_BUCKET)
#         self.bucket = GCPPrivateMediaStorage()
#         self.file = file
#         self.BASE_UPLOAD_PATH = base_upload_path() if base_upload_path else self.BASE_UPLOAD_PATH
#
#     def upload(self):
#         # temporary_file = StringFile(
#         #     name=self.resume.name,
#         #     mime_type=self.resume.content_type,
#         # )
#         # temporary_file = self.bucket.open(self.file.name, 'wb')
#
#         # map(lambda chunk: temporary_file.write(chunk, append_mode=True), self.file.chunks())
#         self.bucket.save(self.file.name, self.file)
#         # self.blob = self.bucket.blob(complete_path)
#         # self.blob.upload_from_file(temporary_file)
#         # return self.BASE_UPLOAD_PATH




