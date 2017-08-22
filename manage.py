#!/usr/bin/env python3
import sys
import argparse

from commands.build import BuildStemAppCommand
from commands.create import CreateStemAppCommand
from commands.custom import CustomStemAppCommand
from commands.initialize import InitializeStemAppCommand
from commands.setup import SetupStemAppCommand
from commands.run import RunStemAppCommand
from commands.publish import PublishStemAppCommand

def colorize(text):
    if not isinstance(text, str):
        # If it's not a string, should be iterable
        return map(colorize, text)
    COLOR_CODE = '\033[95m'
    END_CODE = '\033[0m'
    return COLOR_CODE + text + END_CODE


def main():
    parser = argparse.ArgumentParser(description="Stem App creation and management helper")

    action_type = parser.add_mutually_exclusive_group()
    action_type.add_argument("--create", help="Create a new Stem app",
                             const="",
                             type=str,
                             nargs="?")
    action_type.add_argument("--init", help="Initialize a Stem app from a stem.json", action="store_true")
    action_type.add_argument("--publish", help="Publish app to GitHub", action="store_true")
    action_type.add_argument("--setup",
                             help="Configure a newly cloned app",
                             action="store",
                             choices=["production", "dev"])
    action_type.add_argument("--upgrade", help="Update the project to the latest stem and establishment version",
                             action="store",
                             choices=["app", "establishment", "stem", "npm"])
    action_type.add_argument("-b", "--build", help="Build the current project", action="store_true")
    action_type.add_argument("-w", "--watch", help="Build the project and watch for changes", action="store_true")
    action_type.add_argument("-r", "--run", help="Ensure the project is built in the background and run it", action="store_true")
    action_type.add_argument("--seticon", help="Set a favicon to be used by the website", action="store")
    action_type.add_argument("--deploy", help="Deploy the source code to a remote server", action="store")
    action_type.add_argument("--version", help="Display the helper version", action="version", version="Stem App Manager 0.1.0")

    args = parser.parse_args()

    if args.create is not None:
        CreateStemAppCommand(args.create).run()
        InitializeStemAppCommand().run()
        PublishStemAppCommand().run()
        SetupStemAppCommand(args.setup).run()
        RunStemAppCommand().run()
    elif args.init:
        InitializeStemAppCommand().run()
    elif args.publish:
        PublishStemAppCommand().run(explicit_call=True)
    elif args.setup:
        SetupStemAppCommand(args.setup).run()
    elif args.build:
        BuildStemAppCommand(watch=False).run()
    elif args.watch:
        BuildStemAppCommand(watch=True).run()
        # CustomStemAppCommand("run").run()
    elif args.run:
        RunStemAppCommand().run()
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())
