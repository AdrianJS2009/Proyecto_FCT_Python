from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response



class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict occurred."
    default_code = "conflict"

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found."
    default_code = "not_found"

class UnsupportedCommandException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Unsupported command."
    default_code = "unsupported_command"



def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = extract_message_from_response(response)
        response.data = {
            "code": getattr(exc, 'default_code', 'error'),
            "message": message
        }
    else:
        response = handle_unexpected_error(exc)

    return response


def extract_message_from_response(response):
    if isinstance(response.data, dict):
        if "detail" in response.data:
            return response.data["detail"]
        return flatten_field_errors(response.data)
    return str(response.data)


def flatten_field_errors(data):
    messages = []
    for key, value in data.items():
        if isinstance(value, list):
            messages.extend(value)
        else:
            messages.append(str(value))
    return " ".join(messages)


def handle_unexpected_error(exc):
    return Response({
        "code": "internal_server_error",
        "message": f"Unexpected error occurred: {str(exc)}"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)