import logging


class CmdResult:
    def __init__(self, stdout, stderr, exit_code):
        self.stdout: paramiko.ChannelFile = stdout
        self.stderr: paramiko.ChannelStderrFile = stderr
        self.exit_code: int = exit_code

    def read(self, file):
        file.read().decode("utf-8")

    def log_stdout(self, logger, task_number) -> None:
        lines = self.stdout.read().decode("utf-8").splitlines()
        while "" in lines:
            lines.remove("")

        for line in lines:
            logger("[%d] %s", task_number, line)
