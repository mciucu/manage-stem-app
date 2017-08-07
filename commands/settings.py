import json
import os

import sys


orda = ord('a')
ordA = ord('A')


def to_camel_case(txt):
    capitalise_next = False
    new_txt = ""

    for c in txt:
        if 'A' <= c <= 'Z':
            new_txt += c
        elif capitalise_next and 'a' <= c <= 'z':
            new_txt += chr(ord(c) - orda + ordA)
            capitalise_next = False
        elif c == '_':
            capitalise_next = True
        else:
            capitalise_next = False
            new_txt += c

    return new_txt


def to_underscore_case(txt):
    new_txt = ""

    for c in txt:
        if 'A' <= c <= 'Z':
            new_txt += "_" + chr(ord(c) + orda - ordA)
        else:
            new_txt += c

    return new_txt


class SettingsFileManager(object):
    def __init__(self, file_name, extra=None, die_on_missing=True):
        self.file_name = file_name

        if os.path.isfile(self.file_name):
            with open(file_name) as data_file:
                self.settings = json.load(data_file)
        else:
            if die_on_missing:
                sys.exit("Missing settings file %s" % file_name)
            self.settings = dict()

        if extra:
            self.update(extra, False)

    def update(self, d, with_save):
        # Not a deep copy, for now
        for key in d:
            self.settings[key] = d[key]
        if with_save:
            self.save()

    def get(self, *args, default=None):
        current_value = self.settings
        for index, arg in enumerate(args):
            arg = to_camel_case(arg)
            if arg not in current_value and index == len(args) - 1 and default is not None:
                return default
            current_value = current_value[arg]

        return current_value

    def has(self, *args):
        current_dict = self.settings
        for arg in args:
            arg = to_camel_case(arg)
            if not arg in current_dict:
                return False
            current_dict = current_dict[arg]

        return True

    def set(self, *args):
        current_dict = self.settings

        while len(args) > 2:
            current_dict = current_dict[to_camel_case(args[0])]
            args = args[1:]

        key, value = args
        current_dict[key] = value

        self.save()

    def save(self, file_name=None):
        file_name = file_name or self.file_name
        # First make sure there won't be an error, to not crap after erasing the file
        json.dumps(self.settings)
        # TODO: should probably create a temporary file, and only then move it instead of the current settings file
        with open(file_name, mode="w") as settings_file:
            json.dump(self.settings, settings_file, indent=2, sort_keys=True)
