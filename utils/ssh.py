import paramiko  # https://docs.paramiko.org/en/stable/
import logging
import enum
from utils.cmd_result import CmdResult


class Method(enum.Enum):
    CREDENTIALS = 1
    KEY = 2
    DEFAULT = 3


class SSHClient:
    def __init__(self, params: dict = {}):
        self.session: paramiko.SSHClient = paramiko.SSHClient()
        self.params: dict = params

    def authenticate(self) -> None:
        """Authenticate to a SSH server using the chosen method."""
        if "ssh_user" in self.params and "ssh_password" in self.params:
            self.method = Method.CREDENTIALS
        elif "ssh_key_file" in self.params:
            self.method = Method.KEY
        else:
            self.method = Method.DEFAULT

    def connect(self) -> None:
        """Connect to a SSH server."""
        self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.method is Method.CREDENTIALS:
            self.session.connect(
                hostname=self.params["ssh_address"],
                port=self.params["ssh_port"],
                username=self.params["ssh_user"],
                password=self.params["ssh_password"],
            )
        elif self.method is Method.KEY:
            self.session.connect(
                hostname=self.params["ssh_address"],
                port=self.params["ssh_port"],
                key_filename=self.params["ssh_key_file"],
            )
        else:
            self.session.connect(
                hostname=self.params["ssh_address"], port=self.params["ssh_port"]
            )

    def run(self, command: str) -> CmdResult:
        """Run a command inside the SSH server."""
        stdin, stdout, stderr = self.session.exec_command(command)
        return CmdResult(stdout, stderr, stdout.channel.recv_exit_status())
