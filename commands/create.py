from .base import BaseStemAppCommand

def get_setting_from_console(message):
    print(message)
    return input()


def is_valid_license(app_license):
    return app_license in licenses


def get_license_from_console():
    while True:
        app_license = get_setting_from_console("Enter the license name {} (empty for no license): ".format(licenses))

        if is_valid_license(app_license):
            return app_license

        print("Invalid license. Please try again.")


def check_config_from_file(data):
    if not is_valid_license(data["license"]):
        print("Invalid license. Should be on the list {} (empty for no license): ".format(licenses))
        return
    return data


def get_app_config_from_console(args):
    # short_name = get_setting_from_console("Enter your app's short name: ")
    short_name = args.create;

    long_name = get_setting_from_console("Enter your app's long name: ")
    author = get_setting_from_console("Enter your name: ")
    app_license = get_license_from_console()
    description = get_setting_from_console("Enter your app's description: ")

    return {
        "short_name": short_name,
        "project_name": long_name,
        "author_name": author,
        "license": app_license,
        "project_description": description,
    }


def get_app_config_from_file(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        return check_config_from_file(data)


def get_app_config(args):
    if not os.path.isfile(args.create):
        app_config = get_app_config_from_console(args)
    else:
        app_config = get_app_config_from_file(args.create)

    return app_config



class CreateStemAppCommand(BaseStemAppCommand):
    def __init__(self, project_name):
        self.project_name = project_name
        super().__init__()

    def run(self):
        pass