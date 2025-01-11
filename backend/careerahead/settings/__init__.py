from pathlib import Path
import dotenv
import os
from split_settings.tools import include, optional

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOCAL_SETTING_PATH = os.getenv('LOCAL_SETTING_PATH', 'local/local.settings.py')
LOCAL_SETTING_PATH = LOCAL_SETTING_PATH if os.path.isabs(LOCAL_SETTING_PATH) else str(BASE_DIR / LOCAL_SETTING_PATH)

include(
    'base.settings.py',
    'application.settings.py',
    optional(LOCAL_SETTING_PATH)
)