import time


def get_scheduler_upload_path(instance, filename):
    return "scheduler/{timestr}/{filename}".format(
        timestr=time.strftime("%Y_%m_%d"), filename=filename)