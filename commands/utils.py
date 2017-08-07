import random

import os, sys


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

def require_sudo():
    if not is_sudo():
        sys.exit("Please re-run with administrator rights!")


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

    with open(filename, "r") as content_file:
        template_content = content_file.read()

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
    output_is_template = False

    path_to_without_extension, path_to_extension = os.path.splitext(path_to)

    if path_to_extension == ".noextension":
        path_to = path_to_without_extension
    elif path_to_extension == ".template":
        path_to = path_to_without_extension
        output_is_template = True

    if verbosity >= 2:
        print("Rendering", path_from, "->", path_to)

    output_content = render_template_to_string(path_from, context, output_is_template)

    os.makedirs(os.path.dirname(path_to), exist_ok=True)
    with open(path_to, "w") as rendered_file:
        rendered_file.write(output_content)
