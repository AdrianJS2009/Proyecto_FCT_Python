from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

# Excepciones Personalizadas

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
    # Hay que llamar primero al manejador de excepciones por defecto
    response = exception_handler(exc, context)

    if response is not None:
        #Si hay respuesta con datos, la modificamos
        if isinstance(response.data, list):
            error_message = " ".join(response.data)
        elif isinstance(response.data, dict):
            # He visto que se incluyen "details" como respuesta en ejemplos
            if "detail" in response.data:
                error_message = response.data["detail"]
            else:
                error_message = str(response.data)

        response.data = {
            "code": getattr(exc, 'default_code', 'error'),
            "message": error_message
        }
    else:
        # Alguna excepcion que no controle suelto el 500
        response = Response({
            "code": "internal_server_error",
            "message": f"Unexpected error occurred: {str(exc)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
