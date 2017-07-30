import logging
import os

# Ensure the log folder exists
# TODO: this should be configurable in settings.py
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log")
os.makedirs(LOG_FILE_PATH, exist_ok=True)

from establishment.misc.logging_handlers import JSONFormatter

LOGGING = {
   "version": 1,
   "disable_existing_loggers": False, #TODO: add a default logger, for old stuff
   "formatters": {
       "simple": {
           "format": "[%(asctime)s %(module)s] %(levelname)s: %(message)s"
       },
       "json": {
           "()": JSONFormatter,
           "format": "%(asctime)s %(levelname)s %(message)s %(module)s  %(created)f %(filename)s %(funcName)s %(lineno)d %(processName)s"
       }
   },
   "filters": {
       "require_debug_false": {
           "()": "django.utils.log.RequireDebugFalse",
       },

   },
   "handlers": {
       "console": {
           "level": "DEBUG",
           "class": "logging.StreamHandler",
           "formatter": "simple",
       },
       "redis_handler": {
           "level": "INFO",
           "formatter": "json",
           "class": "establishment.misc.logging_handlers.RedisLoggingHandler",
       },
       "mail_admins": {
           "level": "ERROR",
           "class": "django.utils.log.AdminEmailHandler",
           "filters": ["require_debug_false"],
           "include_html": True,
       },
       "rolling_file_django": {
           "level": "DEBUG",
           "formatter": "json",
           "class": "establishment.misc.logging_handlers.BackgroundRotatingFileHandler",
           "filename": os.path.join(LOG_FILE_PATH, "django.log"),
           "maxBytes": 32 << 20,
           "backupCount": 5,
       },
   },
   "loggers": {
       "django": {
           "handlers": ["redis_handler", "rolling_file_django", "mail_admins"],
           "level": "INFO",
           "propagate": True,
       },
   },
}

LOGGING["loggers"]["default"] = LOGGING["loggers"]["django"]

request_logger = logging.getLogger("django.request")
