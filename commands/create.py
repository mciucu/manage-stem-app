import os
import sys

from commands.settings import SettingsFileManager

from .base import BaseStemAppCommand
from .utils import get_setting_from_console
from .initialize import InitializeStemAppCommand


class CreateStemAppCommand(BaseStemAppCommand):
    LICENSES = []

    def __init__(self, folder_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.folder_name = folder_name

    def get_recommended_project_name(self):
        if self.folder_name:
            return self.folder_name
        _, filename = os.path.split(os.getcwd())

        return filename or "stemapp"

    def load_settings(self):
        self.settings = SettingsFileManager(self.get_setting_file_path(), extra={}, die_on_missing=False)

    def is_valid_license(self, app_license):
        return app_license in self.LICENSES

    def get_license_from_console(self):
        while True:
            app_license = get_setting_from_console("Enter the license name %s (empty for no license)" % self.LICENSES)

            if app_license == "":
                return None

            if self.is_valid_license(app_license):
                return app_license

            print("Invalid license. Please try again.")

    def get_project_settings_from_console(self):
        project_settings = {
            "name": get_setting_from_console("Enter your app name", self.get_recommended_project_name()),
            "author": get_setting_from_console("Enter your name"),
            "description": get_setting_from_console("Enter app description"),
            "license": self.get_license_from_console(),
        }

        # Remove empty settings
        return dict((key, value) for key, value in project_settings.items() if value)

    def run(self):
        if self.folder_name:
            try:
                os.makedirs(self.folder_name)
            except:
                sys.exit("Could not create folder %s (check if you have permissions or if it exists already)." % self.folder_name)
            os.chdir(self.folder_name)

        if os.getcwd() == "/":
            sys.exit("No, I refuse to create a stem app in root.")

        if os.path.isfile("stem.json"):
            sys.exit("A project already exists in %s." % os.getcwd())

        print("Creating a new app in folder " + os.getcwd())

        self.settings.set("project", self.get_project_settings_from_console())

        InitializeStemAppCommand().run()
