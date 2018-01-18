import os
from urllib import parse
from django.core.files.storage import get_storage_class
from storages.backends.gcloud import GoogleCloudStorage
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


class GCPMediaStorage(GoogleCloudStorage):
    """
    GCP storage backend
    """
    bucket_name = settings.GCP_MEDIA_BUCKET

    def url(self, name):
        return settings.MEDIA_URL + name

