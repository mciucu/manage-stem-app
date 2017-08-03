import psycopg2
from commands.base import *
from commands.initialize import render_template
from commands.build import BuildStemAppCommand


# TODO: This is perhaps not the best way to find out whether an app is installed or not (for example python3-dev)
def is_installed(app):
    return subprocess.call("type " + app, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def install_app(app):
    subprocess.check_call(["apt", "install", "-y", app])


def update_apt():
    subprocess.check_call(["apt", "update"])


class SetupStemAppCommand(BaseStemAppCommand):
    def __init__(self, setup_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_type = setup_type
        # TODO: check that we have the settings for this

    def run(self):
        self.install_requirements()

        project_name = self.settings.get("project", "name")

        database_name = project_name
        database_username = "postgres"
        database_userpass = "postgres"

        connection_settings = {"database" : "postgres",
                               "user" : database_username,
                               "password" : database_userpass,
                               "host" : "127.0.0.1",
                               "port" : "5432"}

        database_connection = psycopg2.connect(**connection_settings)
        database_connection.autocommit = True
        database_cursor = database_connection.cursor()

        connection_settings["database"] = database_name
        try:
            database_connection = psycopg2.connect(**connection_settings)
        except psycopg2.OperationalError:
            database_cursor.execute("CREATE DATABASE " + database_name + ";")
            database_connection = psycopg2.connect(**connection_settings)

        database_connection.autocommit = True
        database_cursor = database_connection.cursor()
        database_cursor.execute("GRANT ALL PRIVILEGES ON DATABASE " + database_name + " TO " + database_username + ";")

        if prompt_for("Would you like to import a database?", implicit_yes=False):
            self.import_database(database_cursor)

        database_connection.close()

        context = {
            "secret_key": generate_random_key(length=58),
            "database_name": database_name
        }

        # if self.setup_type == "production":
        # TODO: modify context here

        template_file = self.get_manager_resource("project_template/resources/setup/dev/local_settings.py")
        dest_file = os.path.join(self.get_project_root(), project_name + "/local_settings.py")
        render_template(template_file, dest_file, context)

        self.run_command(["python3", "manage.py", "migrate"])

        if prompt_for("Would you like to create a website account with superuser (admin) rights?"):
            self.run_command(["python3", "manage.py", "createsuperuser"])

        BuildStemAppCommand(watch=False).run()
        # [production] install fail2ban, nginx, etc.
        # [production] setup sysctl.conf and security limits
        # [production] generate a HTTPS key

    def install_requirements(self):
        update_apt()
        if not is_installed("psql"):
            install_app("postgresql")
            install_app("postgresql-server-dev-all")

        apps = [
            "build-essential", "libssl-dev",
            "curl", "redis-server", "g++",
            "net-tools", "python3-dev",
            "libpng-dev", "libjpeg-dev"
        ]

        for app in apps:
            if not is_installed(app):
                install_app(app)

        update_apt()
        if not is_installed("nodejs"):
            self.run_command(["curl", "-sL", "https://deb.nodesource.com/setup_8.x"])
            update_apt()
            install_app("nodejs")

        self.run_command(["npm", "install", "-g", "babel-cli", "rollup"])
        self.run_command(["npm", "install", "--dev"])
        self.run_command(["npm", "install"])
        self.run_command(["easy_install3", "pip"])
        self.run_command(["pip3", "install", "--upgrade", "-r", "requirements.txt"])

    @staticmethod
    def import_database(database_cursor):
        print("Please enter the path to the file")
        file_name = input()
        while not os.path.isfile(file_name) or not file_name.endswith(".sql"):
            print("Invalid file location or file type, please try again..")
            file_name = input()
        # TODO: this is not a proper way to import a database
        database_cursor.execute(open(file_name, "r").read())
