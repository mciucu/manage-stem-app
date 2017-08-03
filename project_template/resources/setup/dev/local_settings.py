DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ database_name }}',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}

DEFAULT_HTTP_PROTOCOL = "http"

WSGI_APPLICATION = 'establishment.websockredis.django_runserver.application'

WEBSOCKET_HEARTBEAT_INTERVAL = 30
WEBSOCKET_HEARTBEAT = "--hrtbeet--"
