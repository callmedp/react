import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def offset_paginator(page, data, **kwargs):
    custom_size = kwargs.get("size", None)
    if custom_size:
        try:
            size = int(custom_size)
        except ValueError:
            size = settings.PAGINATOR_PAGE_SIZE
    else:
        size = settings.PAGINATOR_PAGE_SIZE

    try:
        page = int(page)
        if page <= 0:
            page = 1
    except ValueError:
        page = 1
    if isinstance(data, list):
        total = len(data)
    else:
        total = data.count()
    count = math.ceil(total / size)
    if count == 0:
        page = 1
    else:
        if page > count:
            page = count
    offset = page * size - size
    return {"data": data[offset : size * page], "total": total,"total_pages":count,"current_page":page}