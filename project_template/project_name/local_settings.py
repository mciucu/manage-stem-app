DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': '{{project_name}}',
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

# This setting is required to override the Django's main loop, when running in
# development mode, such as ./manage runserver
WSGI_APPLICATION = "establishment.websockredis.django_runserver.application"

ENABLE_MANAGE_URLS = False
ENABLE_LIVE_WEBSOCKETS = False
FORCE_LIVE = False
