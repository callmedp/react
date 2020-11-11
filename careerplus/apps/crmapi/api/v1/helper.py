from rest_framework.response import Response


def APIResponse(data=None, message=None, status=None):
    resp_json = {
        'message': message,
        'data': data,
        'status': status
    }
    return Response(resp_json, status=status)
