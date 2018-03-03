# import all default settings.
from .settings import *

STATIC_URL = '/static/IMnight/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (
#     'ntu.im/night/2018',
# )
#
# CSRF_TRUSTED_ORIGINS = (
#     'ntu.im/night/2018',
# )

CORS_ALLOW_CREDENTIALS = True


# Allow all host headers.
ALLOWED_HOSTS = ['140.112.106.45', 'ntu.im',
                 'imnight2018.ntu.im', 'imnight2018backend.ntu.im']

# Turn off DEBUG mode.
#DEBUG = False
