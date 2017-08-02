import time

from establishment.baseconfig.models import public_settings_cache


def default(request):
    """
    Adds additional context variables to the default context.
    """
    return {
        "JS_VERSION": getattr(public_settings_cache, "JS_VERSION", 1),
        "SERVER_TIME": time.time(),
    }
