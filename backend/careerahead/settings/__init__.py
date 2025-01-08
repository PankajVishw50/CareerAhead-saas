from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# By default our project runs of Prod mode until specified 
DEBUG = os.getenv("DEBUG", "FALSE").lower() in ('true', 't', '1')

from .base import *

if DEBUG:
    from .dev import * 
else:
    from .prod import * 
