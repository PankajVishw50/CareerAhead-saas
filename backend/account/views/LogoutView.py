from rest_framework.views import APIView
from account.auth import Token
from rest_framework.response import Response
from rest_framework import status

from util.response import ErrorResponseTemplates
from account.models import RefreshToken
from util.dt import now

class LogoutView(APIView):

    def post(self, request):
        # Check the refresh token
        refresh_token = Token.get_refresh_token_from_cookie(request)
        _cookie_passed = False
        if refresh_token:
            _cookie_passed = True
            # It means refresh token was passed in cookie
            if not request.user.is_authenticated:
                return ErrorResponseTemplates.UNAUTHORIZED('Access token is required when refresh_token passed in cookie')
        else:
            refresh_token = Token.get_refresh_token_from_request(request)
            if not refresh_token:
                return ErrorResponseTemplates.UNAUTHORIZED('Refresh token must be provided')
        
        # Validate refresh token
        try:
            refreshtk = RefreshToken.objects.get(code=refresh_token, expiration_on__gt=now)


        except RefreshToken.DoesNotExist:
            return ErrorResponseTemplates.BAD_REQUEST('Invalid refresh token')
        
        # Refresh token should match with user 
        # if was sent through cookies (to protect against csrf attack)
        if _cookie_passed and refreshtk.user != request.user:
            return ErrorResponseTemplates.BAD_REQUEST('Invalid Payload')

        # Delete the refresh token
        refreshtk.delete()

        return Response(None, status.HTTP_200_OK)

        

        

