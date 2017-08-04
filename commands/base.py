import os
import subprocess
import random
from .settings import StemAppSettings


def generate_random_key(length=50, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"):
    rng = random.SystemRandom()
    return ''.join(rng.choice(allowed_chars) for _ in range(length))


def prompt_for(question, implicit_yes=True):
    if implicit_yes:
        print(question + " [Y/n]")
        choice = input().lower()
        if choice.startswith("n"):
            return False
        return True
    else:
        print(question + " [y/N]")
        choice = input().lower()
        if choice.startswith("y"):
            return True
        return False


def valid_input_for(query, on_fail="Please try again: ", is_valid=lambda x: x != ""):
    message = query
    while True:
        print(message, end="")
        x = input()
        if is_valid(x):
            break
        message = on_fail


def is_sudo():
    return os.getuid() == 0


class BaseStemAppCommand(object):
    settings = None
    
    def load_settings(self):
        self.settings = StemAppSettings(self.path)

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

    def get_project_path(self, *paths):
        return os.path.join(self.get_project_root(), *paths)

    def run_command(self, command, path=""):
        path = os.path.join(self.get_project_root(), path)
        if not isinstance(command, list):
            command = list(command)
        return subprocess.check_call(command, cwd=path)

    def run(self):
        raise NotImplementedError("Implement run()")
