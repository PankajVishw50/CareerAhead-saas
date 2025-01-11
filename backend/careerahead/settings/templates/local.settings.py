"""Template file for local settings.

Copy this file to `/local/local.settings.py`
or if you would like to use another path 
you can set it to `LOCAL_SETTING_PATH` environment variable.
"""

DEBUG = False
SECRET_KEY = 'flkewjlfk lkflwefkjw elkfjewlkfjlewkfjlwekfjlewkfjewl'

HOSTED_URL = 'http://localhost:7575'
HOSTED_URL_PREFIX = HOSTED_URL + '/api'
ALLOWED_HOSTS = ['localhost']
