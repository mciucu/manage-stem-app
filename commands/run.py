from commands.base import BaseStemAppCommand
from commands.build import BuildStemAppCommand
from multiprocessing import Process


class RunStemAppCommand(BaseStemAppCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        rollup_proc = Process(target=BuildStemAppCommand(watch=False).run())
        rollup_proc.start()

        django_proc = Process(target=self.run_command(["python3", "manage.py", "runserver"]))
        django_proc.start()


