from rest_framework.views import APIView
from rest_framework.response import Response

from account.auth import Token, get_user_access_token
from util.response import ErrorResponseTemplates
from account.models import RefreshToken
from util.dt import now

class AccessTokenView(APIView):
    authentication_classes = []
    
    def post(self, request):
        # Check if it have refresh token
        if not (refresh_token := Token.get_refresh_token_from_request(request)):
            return ErrorResponseTemplates.UNAUTHORIZED('No refresh token found')

        # Validate refresh token
        try:
            # If no exceptions raised means token is valid
            refreshtk = RefreshToken.objects.get(code=refresh_token, expiration_on__gt=now)

        except RefreshToken.DoesNotExist:
            return ErrorResponseTemplates.BAD_REQUEST()

        # generate access token
        # passing user from refresh token instance 
        # because when refresh_token is passed in body 
        # no need to pass access_token which means no user available
        access_token = get_user_access_token(refreshtk.user, {})

        return Response({
            'access_token': access_token 
        })