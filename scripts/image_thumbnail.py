import os, sys, django, re

# Settings Import
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_live")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

django.setup()

# third party imports
from PIL import Image

# Global Constants
IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG',)

if __name__ == "__main__":

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
