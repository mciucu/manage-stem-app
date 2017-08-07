import json
from .base import *
from .utils import prompt_for, valid_input_for, require_sudo, generate_random_key, render_template, render_template_to_string
from .setup import SetupStemAppCommand

INITIAL_REQUIREMENTS = ["curl", "python", "python3", "git"]
INITIAL_PIP3_REQUIREMENTS = ["jinja2", "psycopg2"]


class InitializeStemAppCommand(BaseStemAppCommand):
    def update_from_settings_file(self, filename):
        template_settings = SettingsFileManager(filename)
        for key in template_settings.settings:
            self.settings.set(key, template_settings.settings[key])

    def init_from_template(self, context):

        template_dir = self.get_manager_resource("project_template")

        project_name = context["project_name"]
        project_main_app = context["project_main_app"]

        for root, dirs, files in os.walk(template_dir):
            for file in files:
                template_file = os.path.join(root, file)

                if template_file == os.path.join(template_dir, "stem.json"):
                    # Do a shallow copy of settings from the stem.json file
                    settings_str = render_template_to_string(template_file, context)
                    settings_dict = json.loads(settings_str)
                    self.settings.update(settings_dict, True)
                    continue

                template_file_relative = os.path.relpath(template_file, template_dir)
                dest_file = os.path.join(self.get_project_root(), template_file_relative)
                dest_file = dest_file.replace("project_name", project_name)
                dest_file = dest_file.replace("/project_main_app/", "/" + project_main_app + "/")
                render_template(template_file, dest_file, context)

    def ensure_packages(self):
        self.get_package_installer().ensure_packages_installed(*INITIAL_REQUIREMENTS)
        self.installer.install_pip()
        self.run_command(["pip3", "install", "--upgrade"] + INITIAL_PIP3_REQUIREMENTS)

    def run(self):
        require_sudo()

        self.ensure_packages()
        project_settings = self.settings.get("project")

        establishment_apps = map(lambda app_name: '"establishment.' + app_name + '"', [
            "accounts",
            "socialaccount",
            "localization",
            "errors",
            "content",
            "baseconfig",
            "documentation",
            # "emailing",
            "chat",
            "blog",
            "forum",
            "misc",
        ])

        context = {
            "author": project_settings["author"],
            "project_name": project_settings["name"],
            "project_main_app": project_settings["name"] + "app",
            "project_description": project_settings["description"],
            "django_version": "1.11",
            "allowed_hosts": '"*"',
            "secret_key": generate_random_key(),
            "establishment_apps": ",\n    ".join(establishment_apps),
            "project_apps": '"' + project_settings["name"] + "app" + '"'
        }

        self.init_from_template(context)

        if not os.path.exists(os.path.join(self.get_project_root(), "establishment")):
            self.run_command(["git", "clone", "https://github.com/establishment/django-establishment", "establishment"])

        SetupStemAppCommand("dev").run()
