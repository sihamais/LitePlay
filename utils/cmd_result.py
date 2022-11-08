import logging


class CmdResult:
    def __init__(self, stdout, stderr, exit_code):
        self.stdout: paramiko.ChannelFile = stdout
        self.stderr: paramiko.ChannelStderrFile = stderr
        self.exit_code: int = exit_code

    def read(self, file):
        file.read().decode("utf-8")

    def log_stdout(self, logger, task_number) -> None:
        stdout_lines = self.stdout.read().decode("utf-8").splitlines()
        while "" in stdout_lines:
            stdout_lines.remove("")

        for line in stdout_lines:
            logger("[%d] %s", task_number, line)

        stderr_lines = self.stderr.read().decode("utf-8").splitlines()
        while "" in stderr_lines:
            stderr_lines.remove("")

        for line in stderr_lines:
            logger("[%d] %s", task_number, line)
