import sys
from .base import *
from .build import BuildStemAppCommand
from .utils import is_sudo, prompt_for, valid_input_for, generate_random_key, render_template

SETUP_NPM_REQUIREMENTS = ["babel-cli", "rollup"]
SETUP_REQUIREMENTS = ["redis-server"]


class SetupStemAppCommand(BaseStemAppCommand):
    def __init__(self, setup_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_type = setup_type
        self.get_package_installer()

    def ensure_database(self, database_name):
        import psycopg2

        if prompt_for("Would you like to change your postgres password for user postgres?", implicit_yes=False):
            database_password = valid_input_for(query="Please enter the new password: ")
            self.run_command(["sudo", "-u", "postgres", "psql", "-c", "ALTER USER postgres WITH PASSWORD '%s';" % database_password])
        else:
            database_password = valid_input_for(query="Please enter the password: ")

        connection_settings = {
            "database": "postgres",
            "user": "postgres",
            "password": database_password,
            "host": "127.0.0.1",
            "port": "5432"
        }

        database_connection = psycopg2.connect(**connection_settings)
        database_connection.autocommit = True
        database_cursor = database_connection.cursor()

        connection_settings["database"] = database_name
        try:
            database_connection = psycopg2.connect(**connection_settings)
        except psycopg2.OperationalError:
            # if the database doesn't exist, creates it
            database_cursor.execute("CREATE DATABASE " + database_name + ";")
            database_connection = psycopg2.connect(**connection_settings)

        database_connection.autocommit = True
        database_cursor = database_connection.cursor()
        database_cursor.execute("GRANT ALL PRIVILEGES ON DATABASE " + database_name + " TO postgres;")

        if prompt_for("Would you like to import a database?", implicit_yes=False):
            file_path = valid_input_for(query="Please enter the path to the file: ",
                                            is_valid=lambda x: os.path.isfile(x) and x.endswith(".sql"))
            self.run_command(["sudo", "-u", "postgres", "psql", database_name, "<", file_path])
        else:
            self.run_command(["python3", "manage.py", "migrate"])
        database_connection.close()

    def run(self):
        self.install_requirements()

        project_name = self.settings.get("project", "name")
        database_name = project_name.lower()

        context = {
            "secret_key": generate_random_key(),
            "database_name": database_name
        }

        # TODO: modify context here
        # if self.setup_type == "production":
        #    install fail2ban, nginx, etc.
        #    setup sysctl.conf and security limits
        #    generate a HTTPS key

        template_file = self.get_manager_resource("project_template/resources/setup/dev/local_settings.py")
        destination_file = self.get_project_path(project_name, "local_settings.py")
        render_template(template_file, destination_file, context)

        self.ensure_database(database_name)

        if prompt_for("Would you like to create a website account with superuser rights? (needed to access the Django admin interface)"):
            self.run_command(["python3", "manage.py", "createsuperuser"])

        BuildStemAppCommand(watch=False).run()

    def install_requirements(self):
        self.installer.install_postgresql()

        self.installer.ensure_packages_installed(*SETUP_REQUIREMENTS)
        self.installer.install_nodejs()

        print("Installing global node requirements", SETUP_NPM_REQUIREMENTS)
        self.run_command(["sudo", "npm", "install", "-g"] + SETUP_NPM_REQUIREMENTS)
        self.run_command(["npm", "install"])
        # TODO: create virtualenv
        self.run_command(["pip3", "install", "--upgrade", "-r", "requirements.txt"])