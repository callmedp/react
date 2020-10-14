from shop.functions import get_file_name

def get_upload_path_order_item_operation(instance, filename):
    return "orderitemoperation/{orderitemoperation_id}/{filename}".format(
        orderitemoperation_id=instance.id, filename=get_file_name(filename))
