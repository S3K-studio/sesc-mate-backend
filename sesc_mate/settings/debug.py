import os
import sys

from .base import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'OPTIONS': {
            'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
        }
    }
}

ALLOWED_HOSTS = [
    'localhost'
]

VK_BOT_TOKEN = os.getenv('DEBUG_VK_BOT_TOKEN')
VK_GROUP_ID = os.getenv('DEBUG_VK_GROUP_ID')
BOT_USERNAME = os.getenv('DEBUG_BOT_USERNAME')

CELERY_DEBUG_MODE = 'sesc_mate.settings.debug'
CELERY_TIMER = '*/1'

""" Debug console logging """

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'logdna': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}
