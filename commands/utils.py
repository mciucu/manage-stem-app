import random

import os

import shutil


def generate_random_key(length=50, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"):
    rng = random.SystemRandom()
    return ''.join(rng.choice(allowed_chars) for _ in range(length))


def prompt_for(question, implicit_yes=True):
    if implicit_yes:
        print(question + " [Y/n] ", end="")
        choice = input().lower()
        if choice.startswith("n"):
            return False
        return True
    else:
        print(question + " [y/N] ", end="")
        choice = input().lower()
        if choice.startswith("y"):
            return True
        return False


def valid_input_for(query, default=None, on_fail="Please try again: ", is_valid=lambda x: x != ""):
    message = query
    while True:
        print(message, end="")
        if default is not None:
            print("[default=" + default +"]", end="")
        print(": ", end="")
        x = input()
        if is_valid(x):
            break
        else:
            if default is not None:
                return default
        message = on_fail
    return x


def is_sudo():
    return os.getuid() == 0


def get_setting_from_console(message, default=None):
    if default:
        message += " (blank={})".format(default)
    print(message, end=": ")

    setting = input()
    if setting == "" and default:
        setting = default

    return setting


def render_template_to_string(filename, context, output_is_template=False):
    import jinja2
    import uuid

    try:
        with open(filename, "r") as content_file:
            template_content = content_file.read()
    except UnicodeDecodeError:
        print("Skipping file %s, as it's non-unicode" % filename)
        return None

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
    return jinja2.Environment().from_string(template_content).render(context)


def render_template(path_from, path_to, context, verbosity=2):
    just_copy = False
    output_is_template = False

    path_to_without_extension, path_to_extension = os.path.splitext(path_to)

    if path_to_extension == ".raw":
        path_to = path_to_without_extension
        just_copy = True
    elif path_to.endswith(".min.js"):
        just_copy = True
    elif path_to_extension == ".noextension":
        path_to = path_to_without_extension
    elif path_to_extension == ".template":
        path_to = path_to_without_extension
        output_is_template = True
    elif path_to_extension == ".jsx":
        output_is_template = True

    if verbosity >= 2:
        print("Rendering", path_from, "->", path_to)

    output_content = not just_copy and render_template_to_string(path_from, context, output_is_template)

    os.makedirs(os.path.dirname(path_to), exist_ok=True)

    if output_content:
        with open(path_to, "w") as rendered_file:
            rendered_file.write(output_content)
    else:
        shutil.copyfile(path_from, path_to)


def to_snake_case(txt):
    orda = ord('a')
    ordA = ord('A')
    ordZ = ord('Z')

    new_txt = ""
    for c in txt:
        if ordA <= ord(c) <= ordZ:
            new_txt += "_" + chr(ord(c) + orda - ordA)
        else:
            new_txt += c

    return new_txt


def dict_to_snake_case(json_dict):
    if not isinstance(json_dict, dict):
        return json_dict
    python_dict = {}
    for key in json_dict:
        python_dict[to_snake_case(key)] = dict_to_snake_case(json_dict[key])
    return python_dict


def clean_name(name):
    name = name.lower()
    return "".join([c for c in name if c.isalnum() or c == "_"])
