import os 

"""Settings which are specific to our application.
Should not include django specific or 3rd party settings here. 
"""

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


# Razorpay

RAZORPAY_USERNAME = os.getenv('RAZORPAY_USERNAME')
RAZORPAY_SECRET = os.getenv('RAZORPAY_SECRET')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')
RAZORPAY_BANKING_ACCOUNT_NUMBER = os.getenv('RAZORPAY_BANKING_ACCOUNT_NUMBER')


PAGE_SIZE = 25
MAX_PAGE_SIZE = 50
MINIMUM_WITHDRAWL = 100
MAXIMUM_WITHDRAWL = 10000

EXCEPTION_RESTRUCTURE = True

