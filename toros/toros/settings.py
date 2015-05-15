"""
Django settings for toros project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

if not DEBUG:
    from local_settings import * 
else:
    #This secret key should be used only for debug mode, use a different one for production
    SECRET_KEY = '4i&$vzscu&53t4dui3o*x_1an&+k(&wgq6+&b&hwd%^&hze+_^'
    ALLOWED_HOSTS = []
    SITE_ID = 1
    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/Chicago'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_comments',
    'stdimage',
    'winnow',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'toros.urls'

WSGI_APPLICATION = 'toros.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

ASTRO_IMAGE_DIR = os.path.join(BASE_DIR, 'astro_images')

LOGIN_URL = '/training/login/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

COMMENTS_ALLOW_PROFANITIES = True

MEDIA_URL = '/media/'
