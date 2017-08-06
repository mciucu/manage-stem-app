import os

from commands.settings import SettingsFileManager
from .base import BaseStemAppCommand


class CreateStemAppCommand(BaseStemAppCommand):
    LICENSES = []

    def load_settings(self):
        self.settings = SettingsFileManager(extra={}, die_on_missing=False)

    def get_setting_from_console(self, message):
        print(message)
        return input()

    def is_valid_license(self, app_license):
        return app_license in self.LICENSES

    def get_license_from_console(self):
        while True:
            app_license = self.get_setting_from_console(
                "Enter the license name {} (empty for no license): ".format(self.LICENSES))

            if app_license == "":
                return None

            if self.is_valid_license(app_license):
                return app_license

            print("Invalid license. Please try again.")

    def get_project_settings_from_console(self):
        project_settings = {
            "name": self.get_setting_from_console("App name"),
            "author": self.get_setting_from_console("Author"),
            "description": self.get_setting_from_console("Description"),
            "license": self.get_license_from_console(),
        }

        # Remove empty settings
        return dict((key, value) for key, value in project_settings.items() if value)

    def run(self):
        print("Creating in current folder", os.getcwd())
        self.settings.set("project", self.get_project_settings_from_console())
