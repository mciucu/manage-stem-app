import subprocess
import urllib.request
from abc import ABC, abstractmethod
from sys import exit
from os import remove
from commands.utils import prompt_for

REQUIRED_NODEJS_VERSION = 6


class Installer(ABC):
    PACKAGE_MANAGER_INSTALL_OPTIONS = ["install"]
    PACKAGE_MANAGER_UPDATE_OPTIONS = ["update"]

    def __init__(self):
        self.ensure_package_manager_is_installed()
        self.have_updated_package_manager = False
        super().__init__()

    def is_installed(self, package):
        return subprocess.call("type " + package, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def get_package_manager_command(self):
        return [self.PACKAGE_MANAGER]

    def run_command(self, args):
        subprocess.check_call(args)

    @abstractmethod
    def install_nodejs(self):
        pass

    @abstractmethod
    def install_postgresql(self):
        pass

    def ensure_package_manager_is_installed(self):
        pass

    def install_pip(self):
        pass

    def should_install_nodejs(self):
        if not self.is_installed("nodejs"):
            return True

        version_output = subprocess.Popen(["nodejs", "--version"], stdout=subprocess.PIPE).stdout
        line = next(line for line in version_output)
        version = line[1:-1].decode().split(".")
        return len(version) == 0 or int(version[0]) < REQUIRED_NODEJS_VERSION

    def install_packages(self, *packages):
        self.update_package_manager()
        self.run_command(self.get_package_manager_command() + self.PACKAGE_MANAGER_INSTALL_OPTIONS + list(*packages))

    def ensure_packages_installed(self, *packages):
        packages_to_install = [package for package in packages if not self.is_installed(package)]
        if len(packages_to_install) > 0:
            self.install_packages(*packages)

    def update_package_manager(self):
        if not self.have_updated_package_manager:
            self.run_command(self.get_package_manager_command() + self.PACKAGE_MANAGER_UPDATE_OPTIONS)
            self.have_updated_package_manager = True


class LinuxInstaller(Installer):
    PACKAGE_MANAGER = "apt"
    PACKAGE_MANAGER_INSTALL_OPTIONS = ["install", "-y"]

    def get_package_manager_command(self):
        return ["sudo", self.PACKAGE_MANAGER]

    def install_postgresql(self):
        if not self.is_installed("psql"):
            self.install_packages(["postgresql", "postgresql-server-dev-all"])

    def install_nodejs(self):
        if self.should_install_nodejs():
            # TODO: Perhaps there is a better way of doing this
            temp_nodejs_file = "stem-app-nodejs-helper.sh"
            urllib.request.urlretrieve("https://deb.nodesource.com/setup_8.x", temp_nodejs_file)
            subprocess.check_call(temp_nodejs_file, shell=True)
            remove(temp_nodejs_file)
            self.have_updated_package_manager = False
            self.install_packages(["nodejs"])

    def install_pip(self):
        if not self.is_installed("pip3"):
            self.run_command(["easy_install3", "pip"])


class MacInstaller(Installer):
    PACKAGE_MANAGER = "brew"

    def ensure_package_manager_is_installed(self):
        if not self.is_installed(self.PACKAGE_MANAGER):
            if prompt_for("Homebrew will be installed at this step. Would like like to continue?"):
                self.run_command(["curl", "-fsSL", "https://raw.githubusercontent.com/Homebrew/install/master/install"])
            else:
                exit()

    def install_postgresql(self):
        if not self.is_installed("psql"):
            self.install_packages(["postgresql"])

    def install_nodejs(self):
        if self.should_install_nodejs():
            self.install_packages(["nodejs"])

    def install_pip(self):
        if not self.is_installed("pip3"):
            exit("Could not locate pip3, please install it manually!")

