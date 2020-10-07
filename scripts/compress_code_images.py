#python imports
import ast,os,django,sys,subprocess,csv


#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports
from django.conf import settings
from django.core.mail import EmailMessage

#local imports

#inter app imports

#third party imports
from PIL import Image

#Global Constants
IMAGE_EXTENSIONS = ('png','jpg','jpeg','PNG','JPG','JPEG',)
MIN_FILE_SIZE_RESTRICTION = 5000

if __name__=="__main__":
    total_original_size = 0
    total_new_size = 0

    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith(IMAGE_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)
            original_file_size = os.stat(file_path).st_size
            if original_file_size < MIN_FILE_SIZE_RESTRICTION:
                print("Skipping file {} due to size restriction".format(file))
                continue
            
            file_extension = file.split(".")[-1]
            file_name = ".".join(file.split(".")[:-1])
            file_path_without_extension = os.path.join(root, file_name)

            img = Image.open(file_path)
            img.save(file_path,optimize=True,quality=80)
            img.close()

            new_file_size = os.stat(file_path).st_size
            print("Old file size : {} bytes".format(original_file_size))
            print("New file size : {} bytes".format(new_file_size))

            total_original_size += original_file_size
            total_new_size += new_file_size

    print("Total file size saved {} bytes".format(total_original_size - total_new_size))






