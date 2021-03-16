import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse


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

class JsonValidationHelper:
    """class for methods which helps in providing validation for data received from client

    Raises:
        Exception: MalformedDataException object

    Returns:
        dict -- Validated Dictionary
    """

    class MalformedDataException(Exception):
        """Custom Exception for Malformed Data made for JsonValidationHelper

        Arguments:
            Exception {Exception} -- Exception object

        Returns:
            MalformedDataException -- MalformedDataException object
        """

        def __init__(self, message="Malformed Data"):
            """Constructor of Malformed Data

            Keyword Arguments:
                message {str} -- message while giving the exception (default: {"Malformed Data"})
            """
            super().__init__(message)
            self._message = message

        def __str__(self):
            return self._message

    @staticmethod
    def validate(post_dict, expected_dict):
        """Validate JSON based on expected dictionary

        Arguments:
            post_dict {dict} -- request.data dictionary given when a POST request is received
            expected_dict {dict} -- expected JSON data

        Raises:
            Exception: [description]

        Returns:
            dict -- dictionary provided
        """
        for key, _ in expected_dict.items():
            if key not in post_dict:
                raise JsonValidationHelper.MalformedDataException(
                    "Malformed Data"
                )
        return post_dict