import sys
import subprocess
import os
import time
from commands.base import BaseStemAppCommand


class BuildStemAppCommand(BaseStemAppCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.with_watch = kwargs.get("watch", False)

    def run(self):
        self.run_command(["npm", "install"])
        rollup_path = self.settings.get("build", "config_path")
        try:
            commands = ["rollup", "-c"]
            if self.with_watch:
                commands.append("--watch")
            #self.run_command(commands, path=rollup_path)
            file_name = self.get_project_path("stem-rollup.log")
            process = subprocess.Popen(commands, stderr=open(file_name, "w+"), cwd=rollup_path)
            while True:
                reader = subprocess.Popen(["tail", "-n", "1", file_name], stdout=subprocess.PIPE)
                message = reader.communicate()[0].decode()
                if not (message == "" or message.startswith("bundl")):
                    process.kill()
                    process = subprocess.Popen(commands, stderr=open(file_name, "w+"), cwd=rollup_path)
                else:
                    if not self.with_watch:
                        break
                    time.sleep(2)

        except KeyboardInterrupt:
            sys.exit("\rStopped building")
