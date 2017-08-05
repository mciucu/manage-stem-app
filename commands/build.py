import sys

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
            self.run_command(commands, path=rollup_path)
        except KeyboardInterrupt:
            sys.exit("\rStopped building")
