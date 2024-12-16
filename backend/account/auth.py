from django.core.signing import dumps, loads
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.utils.functional import SimpleLazyObject
import jwt
import secrets 
import datetime
import pytz 

from util.response import ErrorResponseTemplates
from account.serializers import UserSerializer
from account.models import User

def encrypt(text: str) -> str:
    return dumps(text)

def decrypt(text: str) -> str:
    return loads(text)

def get_user_access_token(user, payload: dict = {}):
    return Token.generate_access_token(UserSerializer(user).data, payload)

class Token:
    TOKEN_REFRESH_EXPIRY_TIME = settings.TOKEN_REFRESH_EXPIRY_TIME
    TOKEN_REFRESH_BYTES = settings.TOKEN_REFRESH_BYTES
    TOKEN_REFRESH_KEY = settings.TOKEN_REFRESH_KEY
    TOKEN_REFRESH_ID_KEY = settings.TOKEN_REFRESH_ID_KEY
    TOKEN_REFRESH_SECURE = settings.TOKEN_REFRESH_SECURE
    TOKEN_REFRESH_SAMESITE = settings.TOKEN_REFRESH_SAMESITE
    TOKEN_REFRESH_HTTP_ONLY = True 
    TOKEN_ACCESS_EXPIRY_TIME = 60 * 30 # 30 MINUTES 
    TOKEN_ACCESS_ALGORITHMS = settings.TOKEN_ACCESS_ALGORITHMS

    token_refresh_expiry_time_td = datetime.timedelta(seconds=TOKEN_REFRESH_EXPIRY_TIME)
    token_access_expiry_time_td = datetime.timedelta(seconds=TOKEN_ACCESS_EXPIRY_TIME)

    def __init__(self):
        pass

    @staticmethod
    def _get_authorization_header(request):
        return request.headers.get('Authorization') or request.headers.get('authorization')

    @staticmethod
    def get_authorization_token(request):
        try:
            bearer, token = Token._get_authorization_header(request).split(' ')
            
            if bearer.lower() == 'bearer' and token:
                return token 

        except:
            return False 

        return False  

    @staticmethod
    def generate_refresh_expiry_time(now=None):
        now = datetime.datetime.now(pytz.utc)
        return now + Token.token_refresh_expiry_time_td

    @staticmethod
    def generate_refresh_token(*kwargs):
        return secrets.token_urlsafe(Token.TOKEN_REFRESH_BYTES)

    @staticmethod
    def decode_access_token(raw_token: str):
        try:
            payload = jwt.decode(raw_token, settings.SECRET_KEY, Token.TOKEN_ACCESS_ALGORITHMS)
            return payload
        except:
            pass 
        return 

    @staticmethod
    def generate_access_token(data: dict, payload={}) -> str:

        token = jwt.encode(
            {
                **payload,
                'data': data, 
                'iat': datetime.datetime.now(pytz.utc),
                'exp': datetime.datetime.now(pytz.utc) + Token.token_access_expiry_time_td,
            }, 
            settings.SECRET_KEY,
            Token.TOKEN_ACCESS_ALGORITHMS[0],
        )
        return token

    @staticmethod
    def set_refresh_token_cookie(response, refresh_token):

        response.set_cookie(
            key=Token.TOKEN_REFRESH_KEY,
            value=encrypt(refresh_token),
            max_age=Token.token_refresh_expiry_time_td,
            secure=Token.TOKEN_REFRESH_SECURE,
            httponly=Token.TOKEN_REFRESH_HTTP_ONLY,
            samesite=Token.TOKEN_REFRESH_SAMESITE
        )
        return response
    
    @staticmethod
    def get_refresh_token_from_cookie(request, refresh_token_key=None):
        try:
            refresh_token_key = refresh_token_key or Token.TOKEN_REFRESH_KEY
            if not (refresh_token := request.COOKIES.get(refresh_token_key)) :
                return False
            
            return decrypt(refresh_token)

        except:
            pass 

        return False

    @staticmethod
    def get_refresh_token_from_request(request):
        return Token.get_refresh_token_from_cookie(request) or request.data.get('refresh_token')

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Ignore if there is no token
        if not (_token := Token.get_authorization_token(request)):
            return 
        
        # Parse token
        if not (token := Token.decode_access_token(_token)):
            raise AuthenticationFailed('Invalid access token')

        # Load user
        user = SimpleLazyObject(lambda: User.objects.get(id=token['data']['id']))

        return (user, token)


def login(request, user, in_body=False, in_cookie=True):
    response = Response()

    # Create Refresh Token
    if not (refresh_token := user.create_refresh_token()):
        return (
            False,
            ErrorResponseTemplates.CONFLICT(
                "Failed to generate refresh_token. It could be due to max refresh token limit is reached."
                "Try to logout from previous devices"
            ),
            {}
        )

    # Create Access Token
    access_token = get_user_access_token(user)

    if in_cookie:
        Token.set_refresh_token_cookie(response, refresh_token.code)


    response.data = {
        'access_token': access_token,
    }

    if in_body:
        response.data['refresh_token'] = refresh_token.code

    return (
        True,
        response,
        response.data 
    )