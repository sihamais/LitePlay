import logging


class CmdResult:
    def __init__(self, stdout, stderr, exit_code):
        self._stdout: paramiko.ChannelFile = stdout
        self._stderr: paramiko.ChannelStderrFile = stderr
        self.exit_code: int = exit_code

    def stdout(self):
        return self._stdout.read().decode("utf-8").rstrip()

    def stderr(self):
        return self._stderr.read().decode("utf-8").rstrip()

    def log_output(self, logger, task_number):
        stdout_lines = self.stdout().splitlines()
        while "" in stdout_lines:
            stdout_lines.remove("")

        for line in stdout_lines:
            logger("[%d] %s", task_number, line)

        stderr_lines = self.stderr().splitlines()
        while "" in stderr_lines:
            stderr_lines.remove("")

        for line in stderr_lines:
            logger("[%d] %s", task_number, line)
