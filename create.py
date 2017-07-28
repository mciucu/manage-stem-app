#!/usr/bin/env python3
import inspect
import os
import sys
import argparse
import subprocess
import json
import multiprocessing

global_requirements = ['babel-cli', 'rollup']
stem_app_settings = None


def colorize(text):
    COLOR_CODE = '\033[95m'
    END_CODE = '\033[0m'
    return COLOR_CODE + text + END_CODE


def prompt_for(question):
    print(question + " [Y/n]")
    choice = input().lower()
    if choice.startswith("n"):
        return False
    return True


def create_app(args):
    executable_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

    project_dir = args.create
    if os.path.exists(project_dir):
        print("Directory {} already exists, not changing it!".format(project_dir))
        return -1

    print("Globally installing {}\n".format(", ".join(map(colorize, global_requirements))))
    subprocess.check_call(['sudo', 'npm', 'install', '-g'] + global_requirements)

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


def build_app(with_watch=False):
    rollup_path = stemapp_settings["build"]["configPath"]
    try:
        commands = ["rollup", "-c"]
        if with_watch:
            commands.append("--watch")
        subprocess.check_call(commands, cwd=rollup_path)
    except KeyboardInterrupt:
        sys.exit("\rStopped building")


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
    action_type.add_argument("-u", "--upgrade", help="Update the project to the latest stem and establishment version",
                             action="store",
                             choices=["app", "establishment", "stem", "npm"])
    action_type.add_argument("-b", "--build", help="Build the current project", action="store_true")
    action_type.add_argument("-w", "--watch", help="Build the project and watch for changes", action="store_true")
    action_type.add_argument("-r", "--run", help="Ensure the project is built in the background and run it", action="store_true")
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
