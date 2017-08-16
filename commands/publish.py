import json, sys
from commands.base import *
from commands.utils import prompt_for, valid_input_for, is_sudo, generate_random_key


INITIAL_REQUIREMENTS = ["curl", "git"]


class PublishStemAppCommand(BaseStemAppCommand):
    def run(self, explicit_call=False):
        should_publish = explicit_call

        if not explicit_call:
            if self.settings.has("sourceControl"):
                should_publish = False
                self.settings.set("sourceControl", {})
            else:
                should_publish = prompt_for("Would you like to publish the project to github?", implicit_yes=True)

        if should_publish:
            self.ensure_packages()
            interface = GitHubInterface()
            interface.run()

    def ensure_packages(self):
        self.get_package_installer().ensure_packages_installed(INITIAL_REQUIREMENTS)


class GitInterface(BaseStemAppCommand):
    def run(self):
        self.init_git()
        self.check_for_remote()
        
        if not self.current_remote_link:
            self.get_user_settings()
            if not self.create_remote_repo():
                return False
        
        self.settings.set("sourceControl", {
            "type": "git",
            "link": self.current_remote_link or self.repo_link
        })
        
        if not self.current_remote_link:
            return self.push_to_remote()
        else:
            return True

    def init_git(self):
        self.run_command("git init", pipe_stdout=True)
        return True

    def get_user_settings(self):
        project_settings = self.settings.get("project")

        self.username = valid_input_for("Enter your GitHub username")
        
        self.repo_name = "*name-here*"
        self.repo_name = valid_input_for("GitHub repository name (ex: " + self.get_repo_link() + ")", default=project_settings["name"])

        self.repo_desription = project_settings["description"]
        self.repo_link = self.get_repo_link()
        return True

    def check_for_remote(self):
        out, err, exit_code = self.run_command("git remote -v", pipe_stdout=True, raise_exception=False)
        out = out.decode("ascii", errors="ignore")
        self.current_remote_link = None
        if out != "":
            all_remotes = out.split("\n")
            for remote in all_remotes:
                if remote.find("origin") != -1:
                    self.current_remote_link = remote.split()[1]

        if self.current_remote_link:
            if prompt_for("[WARNING] This project seems to be already published to " + self.current_remote_link + "."+ 
                    "\nWould you like to publish it somewhere else?", implicit_yes=False):
                self.run_command("git remote remove origin", pipe_stdout=True)
                self.current_remote_link = None
            else:
                return False

        return True

    PUBLISH_REMOTE_OK = 1
    PUBLISH_REMOTE_FAIL = 2
    PUBLISH_REMOTE_RETRY = 3

    def does_remote_repo_exist(self):
        import requests
        request = requests.get(self.repo_link)
        return request.status_code == 200

    def create_remote_repo(self):
        if self.does_remote_repo_exist():
            if prompt_for("It looks like that repository " + self.repo_link + " already exists.\nUse another repository?", implicit_yes=True):
                self.get_user_settings()
                return self.create_remote_repo()
            else:
                return True

        while True:
            status, message = self.create_remote_repo_specialised()
            if status == self.PUBLISH_REMOTE_OK:
                print("Succesfully created repository: ", self.repo_link)
                return True
            else:
                print("Cannot create repository: ", self.repo_link)
                print("Reason: ", message)
                if status == self.PUBLISH_REMOTE_FAIL:
                    return False
                
                if not prompt_for("Try again?", implicit_yes=True):
                    return False

                self.get_user_settings()
 
    def push_to_remote(self):
        self.run_command("git add .")

        # make commit
        out, err, exitcode = self.run_command("git commit -m \"Initial Commit\"", pipe_stdout=True, raise_exception=False)
        if exitcode:
            err = err.decode("ascii", errors="ignore")
            if err.find("nothing to commit, working directory clean") != -1:
                print("Cannot make commit. Error:\n", err)
                return False

        if not self.current_remote_link:
            self.run_command("git remote add origin " + self.repo_link)

        print("Pushing initial commit\t" + (self.current_remote_link or self.repo_link))
        self.run_command("git push -u origin master")


class GitHubInterface(GitInterface):
    def get_repo_link(self):
        return "https://github.com/" + self.username + "/" + self.repo_name

    def create_remote_repo_specialised(self):
        github_request = {
            "name": self.repo_name,
            "description": self.repo_desription
        }

        # make the request using github's api
        print("Enter your GitHub password for " + self.username + " below")
        out, err, exitcode = self.run_command(
                "curl -sS -u " + self.username + " https://api.github.com/user/repos " +
                "-d '" + json.dumps(github_request) + "'", 
                pipe_stdout=True, pipe_stderr=False)

        response = json.loads(out.decode("ascii", errors="ignore"))
        if not "message" in response:
            return self.PUBLISH_REMOTE_OK, ""
        else:
            print(response)
            # the only thing that can be fixed is bad credentials
            if (response["message"] == "Bad credentials"):
                return self.PUBLISH_REMOTE_RETRY, "Wrong username/password."
            else:
                return self.PUBLISH_REMOTE_FAIL, response["message"]

