# import all default settings.
from .settings import *

STATIC_URL = '/static/IMnight/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'night2018.ntu.im',
    "ntu.im",
    'imnight2018backend.ntu.im'
)

CSRF_TRUSTED_ORIGINS = (
    'night2018.ntu.im',
    "ntu.im",
    'imnight2018backend.ntu.im'
)

CORS_ALLOW_CREDENTIALS = True

CORS_REPLACE_HTTPS_REFERER = True

CSRF_COOKIE_DOMAIN = "ntu.im"


# Allow all host headers.
ALLOWED_HOSTS = ['testbackend.ntu.im', '127.0.0.1', '140.112.106.45', 'ntu.im',
                 'imnight2018.ntu.im', 'imnight2018backend.ntu.im']

# Turn off DEBUG mode.
#DEBUG = False
