import psycopg2
import sys
from commands.base import *
from commands.initialize import render_template
from commands.build import BuildStemAppCommand
from commands.installer import LinuxInstaller, MacInstaller


class SetupStemAppCommand(BaseStemAppCommand):
    def __init__(self, setup_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_type = setup_type
        self.get_package_installer()

    def ensure_database(self, database_name):
        if prompt_for("Would you like to change your postgres password for user postgres?", implicit_yes=False):
            database_password = valid_input_for(query="Please enter the new password: ")
            self.run_command(["sudo", "-u", "postgres", "psql", "-c", "\"ALTER USER postgres PASSWORD '%s';\"" % database_password])
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
        if not is_sudo():
            sys.exit("Please re-run with administrator rights!")

        self.install_requirements()

        project_name = self.settings.get("project", "name")
        database_name = project_name

        context = {
            "secret_key": generate_random_key(length=58),
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

        required_packages = ["curl", "redis-server", "git", "python3", "python"]
        packages_to_be_installed = []

        for package in required_packages:
            if not self.installer.is_installed(package):
                packages_to_be_installed.append(package)

        self.installer.install_packages(packages_to_be_installed)
        self.installer.install_nodejs()

        self.run_command(["npm", "install", "-g", "babel-cli", "rollup"])
        self.run_command(["npm", "install"])
        self.installer.install_pip()
        self.run_command(["pip3", "install", "--upgrade", "-r", "requirements.txt"])
