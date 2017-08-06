import os
import subprocess

import sys

from commands.installer import MacInstaller, LinuxInstaller
from .settings import StemAppSettings


class BaseStemAppCommand(object):
    settings = None
    installer = None

    def get_package_installer(self):
        if self.installer:
            return self.installer

        self.installer = MacInstaller() if sys.platform == "darwin" else LinuxInstaller()

        return self.installer

    def load_settings(self):
        self.settings = StemAppSettings(self.get_setting_file_path())

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get("path", ".")
        self.args = kwargs.get("args", object())
        self.verbosity = 10
        self.load_settings()

    def get_manager_resource(self, resource=""):
        import inspect
        class_path = os.path.dirname(os.path.abspath(inspect.stack()[0].filename))
        executable_path = os.path.dirname(class_path)
        return os.path.join(executable_path, resource)

    def get_project_root(self):
        return self.path

    def get_setting_file_path(self):
        return os.path.join(self.get_project_root(), "stemapp.json")

    def get_project_path(self, *paths):
        return os.path.join(self.get_project_root(), *paths)

    def run_command(self, command, path=""):
        path = os.path.join(self.get_project_root(), path)
        if not isinstance(command, list):
            command = list(command)
        return subprocess.check_call(command, cwd=path)

    def run(self):
        raise NotImplementedError("Implement run()")
