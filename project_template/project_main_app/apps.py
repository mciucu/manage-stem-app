from django.apps import AppConfig


class DemoAppConfig(AppConfig):
    name = "{{ project_main_app }}"

    def ready(self):
        pass
