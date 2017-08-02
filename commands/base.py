import os
import subprocess
import random

from .settings import StemAppSettings


def generate_random_key(length=50, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"):
    rng = random.SystemRandom()
    return ''.join(rng.choice(allowed_chars) for _ in range(length))


class BaseStemAppCommand(object):
    settings = None
    
    def load_settings(self):
        self.settings = StemAppSettings(self.path)

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get("path", ".")
        self.args = kwargs.get("args", object())
        self.load_settings()

    def get_manager_resource(self, resource=""):
        import inspect
        class_path = os.path.dirname(os.path.abspath(inspect.stack()[0].filename))
        executable_path = os.path.dirname(class_path)
        return os.path.join(executable_path, resource)

    def get_project_root(self):
        return self.path

    def run_command(self, command, path=""):
        path = os.path.join(self.get_project_root(), path)
        if not isinstance(command, list):
            command = list(command)
        return subprocess.check_call(command, cwd=path)

    def run(self):
        raise NotImplementedError("Implement run()")
