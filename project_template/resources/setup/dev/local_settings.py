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

REDIS_CONNECTION = {
   "host": "localhost",
   "port": 6379,
   "db": 0,
   "password": None,
}

REDIS_CONNECTION_WEBSOCKETS = REDIS_CONNECTION
REDIS_CONNECTION_CACHING = REDIS_CONNECTION
REDIS_CONNECTION_LOGGING = REDIS_CONNECTION
REDIS_CONNECTION_SERVICES = REDIS_CONNECTION
REDIS_CONNECTION_JOBS = REDIS_CONNECTION

DEFAULT_HTTP_PROTOCOL = "http"

WSGI_APPLICATION = "establishment.websockredis.django_runserver.application"

STATIC_FILE_WATCHERS = [
    ("establishment.misc.static_serve_patch.RollupFileServer", None),
]

WEBSOCKET_HEARTBEAT_INTERVAL = 30
WEBSOCKET_HEARTBEAT = "my-heartbeat-will-go-on"
