from .base import *
from .custom import CustomStemAppCommand
from .utils import prompt_for, valid_input_for, generate_random_key, render_template, clean_name


class SetupStemAppCommand(BaseStemAppCommand):
    def __init__(self, setup_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_type = setup_type
        self.get_package_installer()

    def get_config(self):
        return self.settings.get("setup").get(self.setup_type, {})

    def get_dependencies(self):
        return self.get_config().get("dependencies", [])

    def get_npm_dependencies(self):
        return self.get_config().get("npmDependencies", [])

    def requires(self, requirement_name):
        return requirement_name in self.get_dependencies()

    def run_root_sql(self, command):
        self.run_command(["sudo", "-u", "postgres", "psql", "-c", command])

    def create_database_user(self, user, password):
        try:
            self.run_root_sql("CREATE USER %s WITH PASSWORD '%s'" % (user, password))
            self.run_root_sql("ALTER USER %s WITH SUPERUSER" % user)
        except:
            pass

    def create_database(self, database_name, database_user):
        try:
            self.run_root_sql("CREATE DATABASE %s" % database_name)
            self.run_root_sql("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" % (database_name, database_user))
        except:
            pass

    def populate_database(self, database_name):
        if prompt_for("Would you like to import a database?", implicit_yes=False):
            file_path = valid_input_for(query="Please enter the path to the file: ",
                                        is_valid=lambda x: os.path.isfile(x) and x.endswith(".sql"))
            self.run_command(["sudo", "-u", "postgres", "psql", database_name, "<", file_path])

    def run(self):
        self.install_requirements()

        project_name = self.settings.get("project", "name")
        clean_project_name = clean_name(project_name)

        context = {
            "secret_key": generate_random_key(),
            "database_name": clean_project_name,
            "database_user": clean_project_name,
            "database_password": clean_project_name,
        }

        if self.setup_type != "dev":
            context["database_password"] = generate_random_key(20)

        template_file = self.get_manager_resource("project_template/resources/setup/%s/local_settings.py" % self.setup_type)
        destination_file = self.get_project_path(project_name, "local_settings.py")
        render_template(template_file, destination_file, context)

        if self.requires("postgresql"):
            self.create_database_user(context["database_user"], context["database_password"])
            self.create_database(context["database_name"], context["database_user"])

            self.populate_database(context["database_name"])

            if self.setup_type == "dev":
                self.run_command(["python3", "manage.py", "makemigrations"])
                self.run_command(["python3", "manage.py", "migrate"])
                if prompt_for("Would you like to create a website account with superuser rights? (needed to access the Django admin interface)"):
                    self.run_command(["python3", "manage.py", "createsuperuser"])

        extra_commands = self.get_config().get("command", [])
        if not isinstance(extra_commands, list):
            extra_commands = [extra_commands]
        for command in extra_commands:
            if isinstance(command, str):
                command = {"command": command}
            CustomStemAppCommand(command).run()

        CustomStemAppCommand("build").run()

    def install_requirements(self):
        special = ["postgresql", "nodejs", "pip3"]

        if self.requires("postgresql"):
            self.installer.install_postgresql()

        if self.requires("nodejs"):
            self.installer.install_nodejs()

        raw_dependencies = [dependency for dependency in self.get_dependencies() if dependency not in special]
        self.installer.ensure_packages_installed(raw_dependencies)

        if self.requires("nodejs"):
            npm_dependencies = self.get_npm_dependencies()
            if len(npm_dependencies):
                self.run_command(["sudo", "npm", "install", "-g"] + npm_dependencies)
                self.run_command(["npm", "install"])
        # TODO: create virtualenv
        if sys.platform.startswith("linux"):
            self.installer.install_packages(["python3-dev", "build-essential"])

        if self.requires("pip3"):
            self.run_command(["sudo", "pip3", "install", "--upgrade", "-r", "requirements.txt"])
