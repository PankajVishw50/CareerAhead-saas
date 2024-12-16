from rest_framework.views import APIView
from rest_framework import status 
from django.contrib.auth import authenticate

from util.response import response_error, ErrorResponseTemplates
from account.auth import Token, login

class LoginView(APIView):

    def post(self, request):
        # Check if have valid request body 
        try:
            email = request.data['email']
            password = request.data['password']
            request.data.setdefault('in_body', False)
            request.data.setdefault('in_cookie', True)

        except KeyError:
            return response_error(status.HTTP_400_BAD_REQUEST, 'Invalid payload')
        
        # Check if valid credentials 
        if not (user := authenticate(username=email, password=password)):
            return ErrorResponseTemplates.BAD_REQUEST()
        

        # Create Refresh Token
        if not (refresh_token := user.create_refresh_token()):
            return ErrorResponseTemplates.CONFLICT(
                "Failed to generate refresh_token. It could be due to max refresh token limit is reached."
                "Try to logout from previous devices"
            )

        # Log user in 
        logged, response, data = login(request, user, request.data.get('in_body'), request.data.get('in_cookie'))

        return response