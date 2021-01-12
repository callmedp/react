from rest_framework.response import Response

def APIResponse(data=None, message=None, status=None, error=False):
    resp_json = {
        'message': message,
        'data': data,
        'status': status,
        'error': error
    }
    return Response(resp_json, status=status)
