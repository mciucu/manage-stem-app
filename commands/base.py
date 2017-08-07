import os
import subprocess

import sys

from commands.installer import MacInstaller, LinuxInstaller
from .settings import SettingsFileManager


class BaseStemAppCommand(object):
    settings = None
    installer = None

    def get_package_installer(self):
        if self.installer:
            return self.installer

        self.installer = MacInstaller() if sys.platform == "darwin" else LinuxInstaller()

        return self.installer

    def load_settings(self):
        self.settings = SettingsFileManager(self.get_setting_file_path())

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
        return os.path.join(self.get_project_root(), "stem.json")

    def get_project_path(self, *paths):
        return os.path.join(self.get_project_root(), *paths)

    def run_command(self, command, path="", pipe_stdout=False, pipe_stderr=True, merge_stderr_to_stdout=False, raise_exception=True):
        stdout = None
        if pipe_stdout:
            stdout = subprocess.PIPE

        stderr = None
        if merge_stderr_to_stdout:
            stderr= subprocess.STDOUT
        else:
            if pipe_stderr:
                stderr = subprocess.PIPE

        path = os.path.join(self.get_project_root(), path)
        if isinstance(command, list):
            str_command = ""
            for comm in command:
                str_command += comm + " "
            command = str_command

        call = subprocess.Popen(command, cwd=path, stdout=stdout, stderr=stderr, shell=True)
        out, err = call.communicate()
        returncode = call.returncode

        if returncode and raise_exception:
            err = err.decode("ascii", errors="ignore")
            raise Exception("Failed to run: ", command, '\n', err)

        return (out, err, returncode)

    def run(self):
        raise NotImplementedError("Implement run()")
