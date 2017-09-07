from threading import Thread
from copy import deepcopy

from .base import BaseStemAppCommand
from .utils import dict_to_snake_case


class CustomStemAppCommand(BaseStemAppCommand):
    def __init__(self, name="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_name = name

    def get_config(self):
        if isinstance(self.config_name, str):
            return self.settings.get(self.config_name)
        return self.config_name

    def run_command(self, command, path="", pipe_stdout=False, pipe_stderr=False, merge_stderr_to_stdout=False, raise_exception=True, **extra):
        command_dict = extra.pop("command_dict", None)
        if command_dict:
            command = self.concat_command(command)
            command = " ".join([command, self.concat_command(command_dict.get("extraArgs", []))])
        super().run_command(command, path, pipe_stdout, pipe_stderr, merge_stderr_to_stdout, raise_exception, **extra)

    def run_django_command(self, command_dict):
        command = ["python3", "manage.py", command_dict["command"]]
        self.run_command(command, command_dict=command_dict)

    def run_shell_command(self, command_dict):
        self.run_command(**dict_to_snake_case(command_dict), command_dict=command_dict)

    def run_stem_command(self, command_name, command_dict=None):
        extra_args = command_dict.get("extraArgs", []) if command_dict else []
        CustomStemAppCommand(command_name).run(*extra_args)

    def run_command_raw(self, command_dict):
        command = command_dict["command"]
        command_type = command_dict.get("type", "multiple" if type(command) == list else "auto")
        if command_type == "django":
            self.run_django_command(command_dict)
        elif command_type == "stem":
            self.run_stem_command(command_dict["command"], command_dict)
        elif command_type == "multiple":
            sub_commands = command_dict.get("command", [])
            for sub_command in sub_commands:
                self.run_command_with_parallelize_check(sub_command)
        elif command_type == "shell":
            self.run_shell_command(command_dict)
        elif command_type == "auto":
            try:
                self.run_stem_command(command_dict["command"], command_dict)
            except (KeyError, TypeError):
                self.run_shell_command(command_dict)
        else:
            raise Exception("Invalid command type " + command_type)

    def run_command_with_parallelize_check(self, command_dict):
        is_parallelized = command_dict.get("background", False)
        if is_parallelized:
            is_daemon = command_dict.get("daemon", False)
            thread = Thread(target=lambda: self.run_command_raw(command_dict), daemon=is_daemon)
            thread.start()
        else:
            self.run_command_raw(command_dict)

    def run(self, *extra_args):
        config = self.get_config()
        if isinstance(self.config_name, str) and not config.get("isCommand", False):
            raise TypeError("Trying to run a non-command object as a command: " + self.config_name)
        config = deepcopy(config)
        config["extraArgs"] = config.get("extraArgs", []) + list(extra_args)
        self.run_command_with_parallelize_check(config)
