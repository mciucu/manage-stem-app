from django.apps import AppConfig
from django.conf import settings


class MainAppConfig(AppConfig):
    name = "{{ project_main_app }}"

    def ready(self):
        from .utils import gather_public_state
        settings.PUBLIC_STATE_COLLECTORS.append(gather_public_state)
