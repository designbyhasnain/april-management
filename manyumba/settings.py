"""
Django settings for manyumba project.
"""

from pathlib import Path
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary configuration using environment variables
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'pnjkenya'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '475813554894579'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', ''),
    secure=True
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-y6escjnp#-(y7lmf5527&qz^ctib!1%4ib_(x5a989j8zd*5v%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*,5.183.9.97:8030,aprilmanagement.pro').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HouseListing.apps.HouselistingConfig',
    'Portfolio',
    'cloudinary',
    'django.contrib.humanize',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

DATA_UPLOAD_MAX_MEMORY_SIZE = 30242880

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'manyumba.urls'

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

WSGI_APPLICATION = 'manyumba.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email Configuration - Using environment variables for security
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = ['https://aprilmanagement.pro', 'http://aprilmanagement.pro', 'http://127.0.0.1:8000/']

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True

# Social account configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

# Site ID for django-allauth
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_ADAPTER = "HouseListing.adapter.MyLoginAccountAdapter"
SOCIALACCOUNT_ADAPTER = 'HouseListing.adapter.MySocialAccountAdapter'

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True