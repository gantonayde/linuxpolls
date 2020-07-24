"""
Django settings for linuxpolls project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ
from google.oauth2 import service_account

# Load 'linuxpolls/.env'
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Use whitenoise to serve static files
WHITENOISE = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # Linuxpolls apps
    'articles',
    'polls',
    'toolbox',

    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Addon apps
    'django_summernote',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linuxpolls.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'linuxpolls.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#       'default': {
#           'ENGINE': 'djongo',
#           'NAME': 'linuxpolls',
#           'CLIENT': {
#              'host': 'mongodb+srv://genadi:1234@cluster0.smdfw.gcp.mongodb.net/linuxpoll?retryWrites=true&w=majority',
#           }
#       }
#  }

if DEBUG:
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         }
     }
else:
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': env("DATABASE_NAME"),
             'USER': env("DATABASE_USER"),
             'PASSWORD': env("DATABASE_PASSWORD"),
             'HOST': env("DATABASE_HOST"),
             'PORT': env("DATABASE_PORT"),
             }
     }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# IP2Location database settings
IP2LOCATION_PATH = os.path.join(BASE_DIR, env('IP2LOCATION_DIR'))
IP2LOCATION_DBCODE = env('IP2LOCATION_DBCODE')
IP2LOCATION_TOKEN = env("IP2LOCATION_TOKEN")


# Required by django-summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Tell Django where static files are when running 'collectstatic'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT  = os.path.join(BASE_DIR, 'public/static/')
STATIC_URL = '/static/'
if WHITENOISE:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    MIDDLEWARE.insert(1,'whitenoise.middleware.WhiteNoiseMiddleware')

# Media files settings
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media/')
else:
    # Serve media files from Google Cloud Storage
    GS_CREDENTIALS_JSON = env('GS_CREDENTIALS_JSON')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR, GS_CREDENTIALS_JSON))
    DEFAULT_FILE_STORAGE = 'linuxpolls.gcloud.GoogleCloudMediaFileStorage'
    GS_MEDIA_BUCKET_NAME = env('GS_MEDIA_BUCKET_NAME')
    MEDIA_URL = f'https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/'

