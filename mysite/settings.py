"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if 'AZURE' in os.environ:
    DEFAULT_FILE_STORAGE = 'referralroulette.custom_azure.AzureMediaStorage'
    STATICFILES_STORAGE = 'referralroulette.custom_azure.AzureStaticStorage'

    STATIC_LOCATION = "static"
    MEDIA_LOCATION = "media"

    # OLD direct-to-azure-blob FILE ACCESS
    #AZURE_ACCOUNT_NAME = "djangostorage"
    #AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
    #STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    #MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

    # NEW through cloudflare cdn method, CNAME to AZURE_CUSTOM_DOMAIN essentially
    AZURE_ACCOUNT_NAME = "djangostorage"
    AZURE_CUSTOM_DOMAIN = "cdn.referralroulette.com"
    STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_ROOT = os.path.join(BASE_DIR, 'referralroulette/static')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('REFERRALROULETTE_SECRET_KEY')

DEBUG = True
if 'PRODUCTION' in os.environ:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    #SECURE_SSL_REDIRECT = True
    #SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com', 'referralroulette.com']
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'referralroulette',
    'taggit',
    'colorfield',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'storages',

    'tinymce',

    'django_user_agents',
]

LOGIN_REDIRECT_URL = "/"

SITE_ID = 1

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': os.getenv('REFERRALROULETTE_GOOGLE_CLIENT_ID'),
            'secret': os.getenv('REFERRALROULETTE_GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_QUERY_EMAIL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {}
if 'HEROKU' in os.environ:
    # Configure Django App for Heroku.
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600, ssl_require=True)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

RECAPTCHA_SITE_KEY = os.getenv('REFERRALROULETTE_RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('REFERRALROULETTE_RECAPTCHA_SECRET_KEY')