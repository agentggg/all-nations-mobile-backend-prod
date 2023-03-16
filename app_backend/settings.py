"""
Django settings for app_backend project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
testing
"""

import os
import environ
from pathlib import Path
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types['DateTimeField'] = 'datetime' # fix for MySQL 5.5
env = environ.Env()
# reading .env file
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'messageme33uqr880aqgqx1ql$e0hdoyy!vch1miwd9eztyfk5raw'

DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_URL = "http://localhost:8000"

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'graphene_django',
    'app_backend_api',
    'django.contrib.auth',
    'django_extensions',
    'django_twilio',
    'corsheaders',
    'rest_framework',
    # 'django_custom_user_migration',
    'rest_framework.authtoken',
    # instructions says to disable that, but that is the table. so with this 
    # disabled, i don't know where token is suppose to go?
    # yea one sec 
    'django_celery_beat',
    # 'django.contrib.gis',
    'django_guid',
    # 'debug_toolbar',
    # ONLY FOR TESTING
    'imagekit',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

#https://www.stackhawk.com/blog/django-cors-guide/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MEDIA_URL = '/media/'  # or any prefix you choose
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
SERVER_EMAIL = env('EMAIL_HOST')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

ADMINS = [
    ("Stevenson Gerard Eustache", "tech.and.faith.contact@gmail.com")
]
# send emails and debug error to admins
ROOT_URLCONF = 'app_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app_backend/templates')],
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

WSGI_APPLICATION = 'app_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env("ENGINE_NAME"),
        'NAME': env("DATABASE_NAME"), #Database Name
        'USER': env("DATABASE_USER"), #Your Postgresql user
        'PASSWORD': env("DATABASE_PASSWORD"), #Your Postgresql password
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT")
    },
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }    
    }

#https://stackoverflow.com/questions/43612243/install-mysqlclient-for-django-python-on-mac-os-x-sierra/54521244



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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE='UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'app_backend_api/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        "LOCATION": "test_table",
        "OPTIONS": {
            "timeout": 1,
            "MAX_ENTRIES" : 4
        }
    }
}
# #BATTOON CUSTOMER DJANGO.

AUTH_USER_MODEL = "app_backend_api.CustomUser"  # new
# # custom user model database for login

import os
import redis

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_PASSWORD = env('REDIS_PASSWORD')
REDIS_URL = f'redis://{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'


INTERNAL_IPS = [
    "127.0.0.1",
]

CLOUDINARY_URL={
    'CLOUD_NAME':env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY':env('CLOUDINARY_API_KEY'),
    'API_SECRET':env('CLOUDINARY_API_SECRET')
}