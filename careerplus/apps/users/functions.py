import datetime

today_date = datetime.datetime.now().date()


def get_upload_path_user_invoice(instance, filename):
    return "invoice/user/{user_id}/{month}_{year}/{filename}".format(
        user_id=instance.user.id, month=today_date.month,
        year=today_date.year, filename=filename)