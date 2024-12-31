# pylint: skip-file
from decouple import config as loadenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# Deployment
# ==========================================
SECRET_KEY = loadenv('DJANGO_PROD_SECRET_KEY')
DEBUG = loadenv('DJANGO_PROD_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = []
STATIC_URL = 'static/'

# ==========================================
# Database config
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "coreapp.User"
DECIMAL_PLACES = loadenv('DJANGO_PROD_DECIMAL_PLACES', default=2, cast=int)
DATABASES = {
    'default': {
        'ENGINE': loadenv('DJANGO_PROD_DB_ENGINE'),
        'NAME': loadenv('DJANGO_PROD_DB_NAME'),
        'USER': loadenv('DJANGO_PROD_DB_USER'),
        'PASSWORD': loadenv('DJANGO_PROD_DB_PASSWORD'),
        'HOST': loadenv('DJANGO_PROD_DB_HOST'),
        'PORT': loadenv('DJANGO_PROD_DB_PORT'),
    }
}

# ==========================================
# Django misc configuration
# ==========================================
ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = loadenv('DJANGO_PROD_TIME_ZONE')
USE_I18N = True
USE_TZ = loadenv('DJANGO_PROD_USE_TZ', default=True, cast=bool)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.coreapp',
    'apps.accounting'
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
