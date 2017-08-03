import os

from commands.base import BaseStemAppCommand, generate_random_key


def render_template(path_from, path_to, context, verbosity=2):
    import jinja2
    import uuid

    output_is_template = False

    path_to_without_extension, path_to_extension = os.path.splitext(path_to)

    if path_to_extension == ".noextension":
        path_to = path_to_without_extension
    elif path_to_extension == ".template":
        path_to = path_to_without_extension
        output_is_template = True

    if verbosity >= 2:
        print("Rendering", path_from, "->", path_to)

    with open(path_from, "r") as content_file:
        template_content = content_file.read()

    if output_is_template:
        # We're generating a template file itself, escape all the template strings
        # Variables are passed as `${ name }$`
        unique_string = uuid.uuid4().hex

        template_content = template_content.replace("}}", unique_string)
        template_content = template_content.replace("{{", '{{"{{"}}')
        template_content = template_content.replace(unique_string, '{{"}}"}}')
        template_content = template_content.replace("{%", '{{"{%"}}')
        template_content = template_content.replace("%}", '{{"%}"}}')
        template_content = template_content.replace("{#", '{{"{#"}}')
        template_content = template_content.replace("#}", '{{"#}"}}')

        template_content = template_content.replace("}$", unique_string)
        template_content = template_content.replace("${", "{{")
        template_content = template_content.replace(unique_string, "}}")

    # Actually render the template
    template_content = jinja2.Environment().from_string(template_content).render(context)

    os.makedirs(os.path.dirname(path_to), exist_ok=True)
    with open(path_to, "w") as rendered_file:
        rendered_file.write(template_content)


class InitializeStemAppCommand(BaseStemAppCommand):
    def init_from_template(self, context):
        template_dir = self.get_manager_resource("project_template")

        project_name = context["project_name"]
        project_main_app = context["project_main_app"]

        for root, dirs, files in os.walk(template_dir):
            for file in files:
                template_file = os.path.join(root, file)
                # TODO: Check if file is stemapp.json, and if so, add to setting with deep copy
                template_file_relative = os.path.relpath(template_file, template_dir)
                dest_file = os.path.join(self.get_project_root(), template_file_relative)
                dest_file = dest_file.replace("project_name", project_name)
                dest_file = dest_file.replace("/project_main_app/", "/" + project_main_app + "/")
                render_template(template_file, dest_file, context)

        # TODO: this should be a deep copy from the stemapp.json file in the template
        self.settings.set("build", {
            "type": "rollup",
            "configPath": project_main_app + "/js/",
        })

    def run(self):
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
            "project_apps": '"' + project_settings["name"] + "app" + '"',
        }

        self.init_from_template(context)

        if not os.path.exists(os.path.join(self.get_project_root(), "establishment")):
            self.run_command(["git", "clone", "https://github.com/establishment/django-establishment", "establishment"])
