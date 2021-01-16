import os
from django.utils.translation import ugettext_lazy as _
from os.path import dirname

DEBUG = False
ALLOWED_HOSTS = [
    'example.com', '*'
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True