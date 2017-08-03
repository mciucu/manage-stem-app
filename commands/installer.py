import subprocess
from abc import ABC, abstractmethod


class Installer(ABC):
    PACKAGE_MANAGER_INSTALL_OPTIONS = ["install"]
    PACKAGE_MANAGER_UPDATE_OPTIONS = ["update"]

    def __init__(self):
        self.have_updated_package_manager = False
        super().__init__()

    def is_installed(self, package):
        return subprocess.call("type " + package, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def run_command(self, args):
        subprocess.check_call(args)

    @abstractmethod
    def install_nodejs(self):
        pass

    @abstractmethod
    def install_postgresql(self):
        pass

    def install_packages(self, *packages):
        self.run_command([self.PACKAGE_MANAGER] + self.PACKAGE_MANAGER_INSTALL_OPTIONS + list(*packages))

    def update_package_manager(self):
        if not self.have_updated_package_manager:
            self.run_command([self.PACKAGE_MANAGER] + self.PACKAGE_MANAGER_UPDATE_OPTIONS)
            self.have_updated_package_manager = True


class LinuxInstaller(Installer):
    PACKAGE_MANAGER = "apt"
    PACKAGE_MANAGER_INSTALL_OPTIONS = ["install", "-y"]

    def install_postgresql(self):
        if not self.is_installed("psql"):
            self.install_packages(["postgresql", "postgresql-server-dev-all"])

    def install_nodejs(self):
        # TODO: check if the already installed nodejs is outdated
        if not self.is_installed("nodejs"):
            self.run_command(["curl", "-sL", "https://deb.nodesource.com/setup_8.x"])
            self.have_updated_package_manager = False
            self.install_packages(["nodejs"])


class MacInstaller(Installer):
    PACKAGE_MANAGER = "brew"

    def install_postgresql(self):
        if not self.is_installed("psql"):
            self.install_packages(["postgresql"])

    def install_nodejs(self):
        if not self.is_installed("nodejs"):
            self.install_packages(["nodejs"])
