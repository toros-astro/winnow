"""
Django local_settings example.

Use this file as a guide for your local_settings.py for your particular
server.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

# This secret key should be used only for debug mode,
# use a different one for production
SECRET_KEY = 'my_Super_$ecr3T_K3y'
ALLOWED_HOSTS = ['example.com', ]
SITE_ID = 1

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATABASES = {
    'default': {
        'NAME': 'app_data',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'postgres_user',
        'PASSWORD': 's3krit'
    },
}

LOGIN_URL = '/globalurl/login'
STATIC_URL = '/globalurl/static/'
MEDIA_URL = '/globalurl/media/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
