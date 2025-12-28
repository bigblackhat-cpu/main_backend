from .settings import *
from dotenv import load_dotenv
import os
load_dotenv()

DEBUG = True

ALLOWED_HOSTS = ['*']

# Development specific applications
INSTALLED_APPS += [
    # 'debug_toolbar',
    "corsheaders",
    'drf_spectacular',
    'drf_spectacular_sidecar',
    "rest_framework",

    "ocrapp.apps.OcrappConfig",

]

# Development specific middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# database settings for development
DATABASES ={
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DEFAULT_DATABASE_NAME'),
        'USER': os.getenv('DEFAULT_DATABASE_USER'),
        'PASSWORD': os.getenv('DEFAULT_DATABASE_PASSWORD'),
        'HOST': os.getenv('DEFAULT_DATABASE_HOST'),
        'PORT': os.getenv('DEFAULT_DATABASE_PORT'),
    },
    'ocr_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('OCR_APP_DATABASE_NAME'),
        'USER': os.getenv('OCR_APP_DATABASE_USER'),
        'PASSWORD': os.getenv('OCR_APP_DATABASE_PASSWORD'),
        'HOST': os.getenv('OCR_APP_DATABASE_HOST'),
        'PORT': os.getenv('OCR_APP_DATABASE_PORT'),
    }
}

# database routers for development
DATABASE_ROUTERS = ["mysite.db_router.OCRRouter"]

# rest framework settings for development
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# media files settings for development
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'mediastore/'

# static files settings for development
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticstore/'
# cors settings for development

CORS_ALLOWED_ORIGINS  = [    
    os.getenv('CORS_ALLOW_ALL_ORIGINS_1'),
    os.getenv('CORS_ALLOW_ALL_ORIGINS_2'),
]
# CORS_ALLOW_HEADERS


# redis cache settings for development
if os.getenv('REDIS_CACHE_LOCATION'):
    CACHES = {
        'default':{
            'BACKEND': "django_redis.cache.RedisCache",
            'LOCATION': os.getenv('REDIS_CACHE_LOCATION'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'dev_django_cache_'
            # 'TIMEOUT': 60*15,  # 15 minutes
        },
        'task_cache':{
            'BACKEND': "django_redis.cache.RedisCache",
            'LOCATION': os.getenv('REDIS_CACHE_LOCATION_TASK'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            'KEY_PREFIX': 'task_cache_'
        }
    }

# celery settings for development

# openapi settings for development
SPECTACULAR_SETTINGS = {
    'TITLE': 'openapi',
    'DESCRIPTION': 'display some data and project',
    'VERSION': '1.0.0',
    'COMPONENT_SPLIT_REQUEST': True
    # 'SERVE_INCLUDE_SCHEMA': False,
    # # OTHER SETTINGS
    # 'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    # 'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    # 'REDOC_DIST': 'SIDECAR',
}





