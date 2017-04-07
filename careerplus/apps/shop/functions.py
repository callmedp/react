import os
import time

from random import random


def get_file_name(f_obj):
    file_name_tuple = os.path.splitext(f_obj)
    extention = file_name_tuple[len(
        file_name_tuple)-1] if len(file_name_tuple) > 1 else ''
    file_name = str(int(time.time())) + '_' + str(int(random()*9999)) + \
        extention
    return file_name

def get_upload_path_category(instance, filename):
    return "category/{cat_id}/{filename}".format(
        cat_id=instance.id, filename=get_file_name(filename))

