from django.conf import settings


def gather_public_state(state, global_constants, context_dict):
    if hasattr(settings, "WEBSOCKET_HEARTBEAT"):
        global_constants["WEBSOCKET_HEARTBEAT"] = settings.WEBSOCKET_HEARTBEAT

