# python imports
import os, sys, django, re, requests
from io import BytesIO

# Settings Import    # change it to settings_live while push  it to git
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_live")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

django.setup()

# django imports
from django.conf import settings
from django.core.files.storage import default_storage

# third party imports
from PIL import Image

# Global Constants
IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG',)

# inter app imports
from blog.models import Blog, Category, Author

from core.library.gcloud.custom_cloud_storage import GCPMediaStorage, GCPPrivateMediaStorage

if __name__ == "__main__":
    modelList = []
    for blog in Blog.objects.all():
        modelList.append(blog)
    for author in Author.objects.all():
        modelList.append(author)
    for category in Category.objects.all():
        modelList.append(category)

    for obj in modelList:
        if settings.IS_GCP:

            try:
                img = GCPMediaStorage().open(obj.image.name, 'rb')
            except Exception as e:
                print(e)
                continue
            url = GCPMediaStorage().url(obj.image.name)
            match = re.search(r'(.*)(.png?|.jpg?|.jpeg?|.PNG?|.JPG?|.JPEG?)$', obj.image.name)
            if match:
                thumbnail_path = '{}-thumbnail{}'.format(match.group(1), match.group(2))
                temp_path = os.path.join(ROOT_FOLDER, 'careerplus', 'media', thumbnail_path)
                try:
                    dest = open(temp_path, 'wb')
                except Exception as e:
                    print(e)
                    continue
                for chunk in img.chunks():
                    dest.write(chunk)
                dest.close()
                img.close()
                temp_img = Image.open(temp_path)
                temp_img.thumbnail((100, 100))
                temp_img.save(temp_path)
                temp_img = open(temp_path, 'rb')
                upload_image = default_storage.open(thumbnail_path, 'wb')
                for chunk in temp_img:
                    upload_image.write(chunk)
                upload_image.close()
                temp_img.close()
                os.remove(temp_path)

    for root, dirs, files in os.walk(ROOT_FOLDER):
        regex_text = '-thumbnail'
        for file in files:
            if not file.endswith(IMAGE_EXTENSIONS) or re.search(regex_text, file) is not None:
                continue
            file_path = os.path.join(root, file)
            img_dir = file_path[:file_path.rindex('/')]
            file_extension = file.split(".")[-1]
            file_name = ".".join(file.split(".")[:-1])
            file_path_without_extension = os.path.join(root, file_name)
            thumbnail_name = '{}-thumbnail.{}'.format(file_name, file_extension)
            try:
                img = Image.open(file_path)
                img.thumbnail((100, 100))
                img.save(os.path.join(img_dir, thumbnail_name))
            except:
                continue
