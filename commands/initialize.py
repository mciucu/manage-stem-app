import json
from commands.base import *
from commands.utils import prompt_for, valid_input_for, is_sudo, generate_random_key

INITIAL_REQUIREMENTS = ["curl", "python", "python3", "git"]
INITIAL_PIP3_REQUIREMENTS = ["jinja2", "psycopg2"]


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

    def publish_to_github(self):
        project_settings = self.settings.get("project")
        source_control_settings = dict()

        if not prompt_for("Would you like to publish the project to github?", implicit_yes=True):
            self.settings.set("sourceControl", source_control_settings)
            return

        github_name = valid_input_for("Enter your github profile: ")
        github_link = "https://github.com/" + github_name + "/" + project_settings["name"]

        source_control_settings["type"] = "git"
        source_control_settings["link"] = github_link

        try: 
            self.run_command(["git", "init"])
            self.run_command(["git", "add", "."])
            self.run_command(["git", "commit", "-m", "\"Initial Commit\""])
            self.run_command(["git", "remote", "add", "origin", github_link])
        except:
            pass

        # Create the repository
        while 1:
            # read more about github's request optins here: https://developer.github.com/v3/repos/#input
            github_request = {
                    "name": project_settings["name"],
                    "description": project_settings["description"]
                }

            # make the request using github's api
            call = subprocess.Popen(
                "curl -sS -u " + github_name + " https://api.github.com/user/repos " +
                "-d '" + json.dumps(github_request) + "'", 
                stdout=subprocess.PIPE, cwd=self.get_project_root(), shell=True)

            out,err = call.communicate()

            response = json.loads(out.decode("ascii", errors="ignore"))

            # is `message` is present, creation failed
            if not "message" in response:
                print("Succesfully created repository\t", github_link)
                break
            else:
                print("Cannot create repository\t", github_link)
                
                # the only thing that can be fixed is bad credentials
                if (response["message"] == "Bad credentials"):
                    if not prompt_for("Wrong username/password. Try again?", implicit_yes=True):
                        return

                    print("Enter your github profile (blank=" + github_name + "): ", end="")
                    new_github_name = input()
                    if new_github_name != "":
                        github_name = new_github_name
                else:
                    print("Reason:\t", response["message"])
                    return

        self.settings.set("sourceControl", source_control_settings)

        print("Making the initial commit\t" + github_link)
        self.run_command(["git", "push", "-u", "origin", "master"])

    def ensure_packages(self):
        self.get_package_installer().ensure_packages_installed(*INITIAL_REQUIREMENTS)
        self.installer.install_pip()
        self.run_command(["pip3", "install", "--upgrade"] + INITIAL_PIP3_REQUIREMENTS)

    def run(self):
        if not is_sudo():
            sys.exit("Please re-run with administrator rights!")

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

        if not self.settings.has("sourceControl"):
            self.publish_to_github()
