from rest_framework.views import APIView
from rest_framework import status 
from django.contrib.auth import authenticate

from util.response import response_error, ErrorResponseTemplates
from account.auth import Token, login


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        # Check if have valid request body 
        try:
            email = request.data['email']
            password = request.data['password']
            in_body = bool(request.data["in_body"] if "in_body" in request.data.keys() else False)
            in_cookie = bool(request.data["in_cookie"] if "in_cookie" in request.data.keys() else True)

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
        logged, response, data = login(request, user, in_body, in_cookie)

        return response