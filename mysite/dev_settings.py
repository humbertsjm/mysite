from mysite._base_settings import *

# Overrides for dev environtment

SECRET_KEY = loadenv('DJANGO_DEV_SECRET_KEY')
DEBUG = loadenv('DJANGO_DEV_DEBUG', default=False, cast=bool)
DATABASES = {
    'default': {
        'ENGINE': loadenv('DJANGO_DEV_DB_ENGINE'),
        'NAME': BASE_DIR / loadenv('DJANGO_DEV_DB_NAME'),
    }
}

AUTH_PASSWORD_VALIDATORS = []
