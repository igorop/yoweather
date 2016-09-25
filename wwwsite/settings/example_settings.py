from wwwsite.settings.base import *

DEBUG = False
LOCAL_SETTINGS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

STATIC_URL = ""
STATIC_ROOT = ""

ALLOWED_HOSTS = []
