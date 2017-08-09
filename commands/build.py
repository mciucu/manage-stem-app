import sys
import subprocess
import time
from commands.base import BaseStemAppCommand

# TODO: Find this from the project's settings.py
REDIS_CONNECTION = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": None,
}


class BuildStemAppCommand(BaseStemAppCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.with_watch = kwargs.get("watch", False)

    def run(self):
        from redis import StrictRedis

        redis_connection = StrictRedis(**REDIS_CONNECTION)

        self.run_command(["npm", "install"])
        rollup_path = self.settings.get("build", "config_path")
        try:
            commands = ["rollup", "-c"]
            if self.with_watch:
                commands.append("--watch")
            process = subprocess.Popen(commands, stderr=subprocess.PIPE, cwd=rollup_path)
            while True:
                message = process.stderr.readline().decode()
                if message:
                    print(message, end="")
                    if "bundling" in message:
                        redis_connection.setex("bundle-ready", 3 * 60, "N")
                    else:
                        redis_connection.setex("bundle-ready", 60, "Y")
                        if not self.with_watch:
                            break
                time.sleep(2)

        except KeyboardInterrupt:
            sys.exit("\rStopped building")
