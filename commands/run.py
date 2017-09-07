from commands.base import BaseStemAppCommand
from commands.custom import CustomStemAppCommand
from multiprocessing import Process


class RunStemAppCommand(BaseStemAppCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        rollup_proc = Process(target=lambda: CustomStemAppCommand("build").run("--watch"))
        rollup_proc.start()

        def django_runserver():
            self.run_command(["python3", "manage.py", "migrate"])
            self.run_command(["python3", "manage.py", "generate_public_state"])
            self.run_command(["python3", "manage.py", "runserver"])

        django_proc = Process(target=django_runserver)
        django_proc.start()
