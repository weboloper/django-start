import os
from os.path import dirname
from django.utils.translation import ugettext_lazy as _


IS_PRODUCTION = False

if IS_PRODUCTION:
    from .conf.production.settings import *
else:
    from .conf.development.settings import *
    

# BASE_DIR =    dirname(dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')

SECRET_KEY = '3d305kajG5Jy8KBafCMpHwDIsNi0SqVaW'

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Vendor apps
    'bootstrap4',
    'tinymce',
    'taggit',
    'sorl.thumbnail',
    'rest_framework',

    # Application apps
    'core',
    'accounts',
    'page',
    'blog',
    'main',
    'newsletter'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

AUTH_USER_MODEL = 'accounts.User'

"""
MODERATION SETTINGS
"""
AKISMET_API_KEY = 'YOUR_AKISMET_API_KEY'
DELETE_SPAM_COMMENT = False
BAN_NON_CJK = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('zh-Hans', _('Simplified Chinese')),
]

TIME_ZONE = 'UTC'
USE_TZ = True


# ROOTS MUST BE ON MAIN DIRECTORY !!!
STATIC_ROOT = '/home/USERNAME/DOMAIN_FOLDER/static'
STATIC_URL = '/static/'

STATIC_ROOT = '/home/USERNAME/DOMAIN_FOLDER/media'
MEDIA_URL = '/media/'


if DEBUG :
    STATIC_ROOT = os.path.join(CONTENT_DIR, 'static')
    MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(CONTENT_DIR, 'assets'),
]

LOCALE_PATHS = [
    os.path.join(CONTENT_DIR, 'locale')
]

ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = False
LOGIN_VIA_EMAIL_OR_USERNAME = True
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'accounts:log_in'
USE_REMEMBER_ME = False

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = True
EMAIL_ACTIVATION_AFTER_CHANGING = True

SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2']

 
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 300,
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | link | image  media | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | code |   help",
    "images_upload_url": '/upload_attachment_url/',

    # URL settings
    'convert_urls' : True,
    'relative_urls' : False,
    'remove_script_host' : False,
}
# TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js'
# TINYMCE_JS_URL = os.path.join(MEDIA_URL, "path/to/tinymce/tinymce.min.js")
# TINYMCE_COMPRESSOR = False

DEFAULT_RENDERER = ['rest_framework.renderers.JSONRenderer', ]
if DEBUG:
    DEFAULT_RENDERER.append('rest_framework.renderers.BrowsableAPIRenderer')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
CORS_ORIGIN_ALLOW_ALL = True

MAILCHIMP_API_KEY = ''
MAILCHIMP_DATA_CENTER = ''
MAILCHIMP_EMAIL_LIST_ID = ''