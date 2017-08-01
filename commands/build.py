from commands.base import BaseStemAppCommand


class BuildStemAppCommand(BaseStemAppCommand):
    def run(self):
        rollup_path = self.settings.get("build", "config_path")
        print("Rollup path", rollup_path)
