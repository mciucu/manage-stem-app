import os

from .settings import StemAppSettings


class BaseStemAppCommand(object):
    def __init__(self, *args, **kwargs):
        self.path = kwargs.get("path", ".")
        self.args = kwargs.get("args", object())
        self.settings = StemAppSettings(self.path)

    def get_manager_resource(self, resource=""):
        import inspect
        class_path = os.path.dirname(os.path.abspath(inspect.stack()[0].filename))
        executable_path = os.path.dirname(class_path)
        return os.path.join(executable_path, resource)

    def get_project_root(self):
        return self.path

    def run(self):
        raise NotImplementedError("Implement run()")
