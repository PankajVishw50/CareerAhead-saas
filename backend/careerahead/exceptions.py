from rest_framework.views import exception_handler  
from account.auth import ErrorResponseTemplates  
from django.conf import settings

def api_exception_handler(exc, context):
    """Converts Exceptions into standard format
    of this API
    {
        "error": {
            "status_code": 400,
            "message": "bad request",
            "messages": ["invalid payload", "no `name` parameter passed"]
        }
    } 
    """
    # Ignore in debug mode
    if not settings.DEBUG_ERROR_HANDLING:
        return

    # import ipdb;ipdb.set_trace()
    try:
        response = exception_handler(exc, context)

        if response is not None:
            payload = {
                'status_code': response.status_code,
                'message': response.data if isinstance(response.data, str) else 'Something went wrong',
            }

            if isinstance(response.data, dict):
                payload['message'] = response.data.get('detail', 'Something went wrong')
            elif isinstance(response.data, list):
                payload['messages'] = response.data 
                            
            response.data = {
                "error": {
                    **payload,
                }
            }

            return response
    except:
        pass 

    return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()