import os
import warnings
from django.utils.translation import ugettext_lazy as _
from os.path import dirname

warnings.simplefilter('error', DeprecationWarning)

DEBUG = True
ALLOWED_HOSTS = ['*',]



EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(CONTENT_DIR, 'tmp/emails')
EMAIL_HOST_USER = 'test@example.com'
DEFAULT_FROM_EMAIL = 'test@example.com'
