import os
from urllib import parse
from django.core.files.storage import get_storage_class
from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings

from google.cloud import storage

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


# class GoogleCloudResumeUploader(object):
#
#     GCP_SECRET_FILE = settings.GCP_SECRET_FILE
#     GCP_BUCKET = settings.GCP_MEDIA_BUCKET
#     BASE_UPLOAD_PATH = settings.GCP_UPLOADS_DIR
#
#     def __init__(self, file, resume_id, candidate_id, base_upload_path=None):
#         # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.GCP_SECRET_FILE
#         self.storage_client = storage.Client()
#         self.bucket = self.storage_client.bucket(self.GCP_BUCKET)
#
#         self.resume, self.resume_id, self.resume_name = resume, str(resume_id), str(resume)
#         self.candidate_id = str(candidate_id)
#
#         self.BASE_UPLOAD_PATH = base_upload_path or self.BASE_UPLOAD_PATH
#
#     def upload(self):
#         path_info = FilePathGenerator(self.resume_id, self.candidate_id, self.resume_name, self.BASE_UPLOAD_PATH).generate_file_path_info()
#         self.store_on_gcp(path_info['complete_path'])
#         return path_info
#
#     def store_on_gcp(self, complete_path):
#         temporary_file = StringFile(
#                 name = self.resume.name,
#                 mime_type = self.resume.content_type,
#             )
#
#         map(lambda chunk: temporary_file.write(chunk, append_mode = True), self.resume.chunks())
#
#         self.blob = self.bucket.blob(complete_path)
#         self.blob.upload_from_file(temporary_file)
