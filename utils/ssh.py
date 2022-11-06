import paramiko  # https://docs.paramiko.org/en/stable/
import logging
import enum


class Method(enum.Enum):
    CREDENTIALS = 1
    KEY = 2
    DEFAULT = 3


class CmdResult:
    def __init__(self, stdout, stderr, exit_code):
        self.stdout: paramiko.ChannelFile = stdout
        self.stderr: paramiko.ChannelStderrFile = stderr
        self.exit_code: int = exit_code

    @property()
    def exit_code(self) -> int:
        return self.exit_code

    def log_output(self) -> None:
        for line in self.stdout.read().splitlines():
            logging.info(line.decode("utf-8"))


class SSHClient:
    def __init__(self, params: dict = {}):
        try:
            self.session: paramiko.SSHClient = paramiko.SSHClient()
            self.params: dict = params
        except paramiko.ChannelException as exception:
            logging.debug(exception.with_traceback())
            logging.error("An error has occured.")

    def authenticate(self) -> None:
        """Authenticate to a SSH server using the chosen method."""
        if self.params["ssh_user"] and self.params["ssh_password"]:
            self.method = Method.CREDENTIALS
        elif self.params["ssh_key_file"]:
            self.method = Method.KEY
        else:
            self.method = Method.DEFAULT

    def connect(self, hostname: str, port: int) -> None:
        """Connect to a SSH server."""
        try:
            if self.method is Method.CREDENTIALS:
                self.session.connect(
                    hostname=hostname,
                    port=port,
                    username=self.params["ssh_user"],
                    password=self.params["ssh_password"],
                )
            elif self.method is Method.KEY:
                self.session.connect(
                    hostname=hostname,
                    port=port,
                    key_filename=self.params["ssh_key_file"],
                )
            else:
                self.session.connect(hostname=hostname, port=port)
        except paramiko.SSHException as exception:
            logging.debug(exception.with_traceback())
            logging.error("An error has occured.")

    def run(self, command: str) -> CmdResult:
        """Run a command inside the SSH server."""
        try:
            stdin, stdout, stderr = self.session.exec_command(command)
            return CmdResult(stdout, stderr, stdout.channel.recv_exit_status)
        except paramiko.SSHException as exception:
            logging.debug(exception.with_traceback())
            logging.error(exception)
