import os
import subprocess

import sys

from commands.base import BaseStemAppCommand


class BuildStemAppCommand(BaseStemAppCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.with_watch = kwargs.get("watch", False)

    def run(self):
        subprocess.check_call(["npm", "install"], cwd=self.get_project_root())
        rollup_path = self.settings.get("build", "config_path")
        rollup_path = os.path.join(self.get_project_root(), rollup_path)
        try:
            commands = ["rollup", "-c"]
            if self.with_watch:
                commands.append("--watch")
            subprocess.check_call(commands, cwd=rollup_path)
        except KeyboardInterrupt:
            sys.exit("\rStopped building")
