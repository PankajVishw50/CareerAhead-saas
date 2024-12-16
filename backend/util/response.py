from rest_framework.response import Response
from rest_framework import status

def response_error(
        status_code=500, 
        message='Something Went wrong',
        data={}
):
    return Response(
        {
            'error': {
                'status_code': status_code,
                'message': message,
                **data,
            }
        },
        status_code
    )

def required_fields_str(fields: list, prefix: str = 'Required fields'):
    return '%s - %s' % (prefix, ', '.join(fields))

def _create_error_response(status_code: int = 500, message: str = 'Something went wrong'):
    return lambda message=message, data={}: response_error(status_code, message, data)

class ErrorResponseTemplates:
    INTERNAL_SERVER_ERROR = _create_error_response(500, 'Something went wrong')
    BAD_REQUEST = _create_error_response(status.HTTP_400_BAD_REQUEST, 'Bad Request')
    UNAUTHORIZED = _create_error_response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized request')
    FORBIDDEN = _create_error_response(status.HTTP_403_FORBIDDEN, 'Request refused')
    NOT_FOUND = _create_error_response(status.HTTP_404_NOT_FOUND, 'Not found')
    METHOD_NOT_ALLOWED = _create_error_response(status.HTTP_405_METHOD_NOT_ALLOWED, 'Method not allowed')
    CONFLICT = _create_error_response(status.HTTP_409_CONFLICT, 'Conflict')

