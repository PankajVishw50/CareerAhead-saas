import os 
from . import BASE_DIR

SECRET_KEY = os.getenv('SECRET_KEY')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',

    'account',
    'wallet',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'careerahead.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'careerahead.context.razorpay_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'careerahead.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },

}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'account.auth.TokenAuthentication',
    ],
    'EXCEPTION_HANDLER': 'careerahead.exceptions.api_exception_handler',
}



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AWS S3 Settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = True 
AWS_LOCATION = 'files/' 
AWS_QUERYSTRING_AUTH = False

AUTH_USER_MODEL = 'account.User'

# EMAIL
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'true').lower() in ('true', 't', '1')
EMAIL_LOG = False
EMAIL_DEBUG_REDIRECT = False
EMAIL_DEBUG_RECEIVERS = []
EMAIL_VERIFICATION_CODE_EXPIRY = 60 * 60 * 24 # One Day 

HOSTED_DOMAIN = os.getenv('HOSTED_DOMAIN')
HOSTED_URL_PREFIX = os.getenv('HOSTED_URL_PREFIX')


# Tokens config
TOKEN_REFRESH_EXPIRY_TIME = (60 * 60 * 24) * 30 # 30 DAYS
TOKEN_REFRESH_BYTES = 64
TOKEN_REFRESH_KEY = os.getenv('TOKEN_REFRESH_KEY', '--rt-k')
TOKEN_REFRESH_ID_KEY = os.getenv('TOKEN_REFRESH_ID_KEY', '_longtid')
TOKEN_REFRESH_SECURE = True  # Only allows https network (except request from localhost domain)
TOKEN_REFRESH_SAMESITE = 'lax' # available options: samesite, lax, none
TOKEN_REFRESH_HTTP_ONLY = True 
TOKEN_ACCESS_EXPIRY_TIME = 60 * 30 # 30 MINUTES 
TOKEN_ACCESS_ALGORITHMS = ['HS256']
TOKEN_REFRESH_MAX_NUMBER_IN_DB = 25
SIGNED_URL_AUTH_MAX_AGE = 60 * 3 # 3 MINUTES
SIGNED_URL_AUTH_TOKEN_KEY = 'token'

ALLOWED_HOSTS = ['*']

# Razorpay

RAZORPAY_USERNAME = os.getenv('RAZORPAY_USERNAME')
RAZORPAY_SECRET = os.getenv('RAZORPAY_SECRET')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')
RAZORPAY_BANKING_ACCOUNT_NUMBER = os.getenv('RAZORPAY_BANKING_ACCOUNT_NUMBER')


PAGE_SIZE = 25
MAX_PAGE_SIZE = 50
MINIMUM_WITHDRAWL = 100
MAXIMUM_WITHDRAWL = 10000

DEBUG_ERROR_HANDLING = False

STATIC_ROOT = 'staticfiles/'