from rest_framework.response import Response
import re


def APIResponse(data=None, message=None, status=None, error=None):
    resp_json = {
        'message': message,
        'data': data,
        'status': status,
        'error': error
    }
    return Response(resp_json, status=status)


international_regex = '(([+][(]?[0-9]{1,3}[)]?)|([(]?[0-9]{4}[)]?))\s*[)]?[-\s\.]?[(]?[0-9]{1,3}[)]?([-\s\.]?[0-9]{' \
                      '3})([-\s\.]?[0-9]{3,4})'
national_regex = '(0/91)?[7-9][0-9]{9}'


def isValidPhone(number):
    return bool(re.match(international_regex, number)) or bool(re.match(national_regex, number))