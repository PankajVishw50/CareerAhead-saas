
from . import BASE_DIR
import os 

ALLOWED_HOSTS = ['*']

# Email
EMAIL_LOG = True

## If it's set to false no email will be sent in debug mode
EMAIL_DEBUG_REDIRECT = os.getenv('EMAIL_DEBUG_REDIRECT', 'false').lower() in ('true', 't', '1')
## Email addresses where email should be redirected to
EMAIL_DEBUG_RECEIVERS = os.getenv('EMAIL_DEBUG_RECEIVERS', '').split('|')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
    }
}

TOKEN_REFRESH_MAX_NUMBER_IN_DB = 50
SIGNED_URL_AUTH_MAX_AGE = 60 * 10 # 10 minutes
CORS_ALLOW_ALL_ORIGINS = True