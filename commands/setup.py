from .base import *
from .build import BuildStemAppCommand
from .utils import prompt_for, valid_input_for, generate_random_key, render_template, clean_name

SETUP_NPM_REQUIREMENTS = ["babel-cli", "rollup"]
SETUP_REQUIREMENTS = ["redis-server"]


class SetupStemAppCommand(BaseStemAppCommand):
    def __init__(self, setup_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_type = setup_type
        self.get_package_installer()

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

        self.create_database_user(context["database_user"], context["database_password"])
        self.create_database(context["database_name"], context["database_user"])

        self.populate_database(context["database_name"])

        if self.setup_type == "dev":
            self.run_command(["python3", "manage.py", "migrate"])
            if prompt_for("Would you like to create a website account with superuser rights? (needed to access the Django admin interface)"):
                self.run_command(["python3", "manage.py", "createsuperuser"])

        BuildStemAppCommand(watch=False).run()

    def install_requirements(self):
        self.installer.install_postgresql()

        self.installer.ensure_packages_installed(SETUP_REQUIREMENTS)
        self.installer.install_nodejs()

        print("Installing global node requirements", SETUP_NPM_REQUIREMENTS)
        self.run_command(["sudo", "npm", "install", "-g"] + SETUP_NPM_REQUIREMENTS)
        self.run_command(["npm", "install"])
        # TODO: create virtualenv
        if sys.platform.startswith("linux"):
            self.installer.install_packages(["python3-dev", "build-essential"])
        self.run_command(["sudo", "pip3", "install", "--upgrade", "-r", "requirements.txt"])
