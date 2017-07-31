#!/usr/bin/env python3
import inspect
import os
import sys
import argparse
import subprocess
import json
import multiprocessing

global_npm_requirements = ['babel-cli', 'rollup']
stem_app_settings = None


def colorize(text):
    if not isinstance(text, str):
        # If it's not a string, should be iterable
        return map(colorize, text)
    COLOR_CODE = '\033[95m'
    END_CODE = '\033[0m'
    return COLOR_CODE + text + END_CODE


def prompt_for(question):
    print(question + " [Y/n]")
    choice = input().lower()
    if choice.startswith("n"):
        return False
    return True


def render_template(path_from, path_to, context):
    import jinja2

    with open(path_from, "r") as content_file:
        template_content = content_file.read()
    rendered_content = jinja2.Environment().from_string(template_content).render(context)
    with open(path_to, "w") as rendered_file:
        rendered_file.write(rendered_content)


def create_app(args):
    executable_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

    project_dir = args.create
    if os.path.exists(project_dir):
        print("Directory {} already exists, not changing it!".format(project_dir))
        return -1

    template_dir = "project_template"

    for root, dirs, files in os.walk(template_dir):
        print(root, dirs, files)

    return

    print("Globally installing {}\n".format(", ".join(colorize(global_npm_requirements))))
    subprocess.check_call(['sudo', 'npm', 'install', '-g'] + global_npm_requirements)

    print("Installing requirements with npm\n")
    subprocess.check_call(['npm', 'update'], cwd=project_dir)

    print("Compiling\n", end='', flush=True)
    subprocess.check_call(['npm', 'run-script', 'build'], cwd=project_dir)

    if prompt_for("Do you want to install redis?"):
        install_redis()
    if prompt_for("Do you want to install postgres?"):
        install_postgres()

    print("\nSuccessfully created project {} at {}".format(colorize(project_dir), colorize(os.path.abspath(project_dir))))
    print("Check out the README located there")
    print("\nInside that directory, you can run\n")
    print("\tnpm start")
    print("\t\tto start a simple development server\n")

    print("\tnpm run-script watch")
    print("\t\tto watch for changes and recompile\n")

    print("Also try {} --help for more options (such as express or django backend)".format(sys.argv[0]))


def ensure_stem_app():
    global stemapp_settings
    if os.path.isfile("stemapp.json"):
        with open("stemapp.json") as data_file:
            stemapp_settings = json.load(data_file)
    else:
        sys.exit("Missing stemapp.json config")


def upgrade_app(args):
    if args.upgrade == "npm":
        pass


def deploy_to_server(args):
    pass


def install_redis():
    subprocess.check_call(["apt", "update"])
    subprocess.check_call(["apt", "install", "redis-server"])


def install_postgres():
    subprocess.check_call(["apt", "install", "postgresql"])


def update_python_requirements():
    # TODO: check that requirements.txt exists and that pip/pip3 are installed
    subprocess.check_call(["pip3", "install", "--upgrade", "-r", "requirements.txt"])


def build_app(with_watch=False):
    rollup_path = stemapp_settings["build"]["configPath"]
    try:
        commands = ["rollup", "-c"]
        if with_watch:
            commands.append("--watch")
        subprocess.check_call(commands, cwd=rollup_path)
    except KeyboardInterrupt:
        sys.exit("\rStopped building")


def setup_app(args):
    setup_type = args.setup
    context = {
        "secret_key": "123"
    }
    # Check if postgres and redis are not installed and offer to install them
    # Install npm and python dependencies
    # Create files in .gitignore (local_settings.py)
    # Generate a new DB, if needed
    # Ask if user wants to import a DB from somewhere
    # Apply migrations to DB
    # Create a new superuser account (if desired)
    # Build the js
    # [production] install fail2ban, nginx, etc.
    # [production] setup sysctl.conf and security limits
    # [production] generate a HTTPS key


def run_server():
    try:
        subprocess.check_call(["python3", "manage.py", "runserver"])
    except KeyboardInterrupt:
        sys.exit("\rStopped running")


def run_app(args):
    stem_builder = multiprocessing.Process(target=build_app, args=[True])
    stem_builder.start()

    server_runner = multiprocessing.Process(target=run_server)
    server_runner.start()


def main():
    parser = argparse.ArgumentParser(description="Stem App creation and management helper")

    action_type = parser.add_mutually_exclusive_group()
    action_type.add_argument("-c", "--create", help="Create a new Stem app", action="store")
    action_type.add_argument("-s", "--setup",
                             help="Configure a newly clones app",
                             action="store",
                             choices=["production", "dev"])
    action_type.add_argument("-u", "--upgrade", help="Update the project to the latest stem and establishment version",
                             action="store",
                             choices=["app", "establishment", "stem", "npm"])
    action_type.add_argument("-b", "--build", help="Build the current project", action="store_true")
    action_type.add_argument("-w", "--watch", help="Build the project and watch for changes", action="store_true")
    action_type.add_argument("-r", "--run", help="Ensure the project is built in the background and run it", action="store_true")
    action_type.add_argument("--seticon", help="Set a favicon to be used by the website", action="store")
    action_type.add_argument("-d", "--deploy", help="Deploy the source code to a remote server", action="store")
    action_type.add_argument("-v", "--version", help="Display the helper version", action="version", version="Stem App Manager 0.1.0")

    args = parser.parse_args()
    if args.create:
        create_app(args)

    ensure_stem_app()

    if args.upgrade:
        upgrade_app(args)

    if args.deploy:
        deploy_to_server(args)

    if args.build:
        build_app()

    if args.watch:
        build_app(True)

    if args.run:
        run_app(args)


if __name__ == "__main__":
    sys.exit(main())
