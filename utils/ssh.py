import paramiko


class SSH:
    def __init__(self):
        try:
            ssh_client = paramiko.SSHClient()
        except paramiko.ChannelException as exception:
            logging.debug(exception.with_traceback())
            logging.error("An error has occured.")
        else:
            self.client = ssh_client

    def authenticate(self, method):
        """Authenticate to a SSH server using the chosen method."""

    def connect(self, hostname: str, port: int):
        """Connect to a SSH server."""
        try:
            self.client.connect(hostname, port)
        except paramiko.SSHException as exception:
            logging.debug(exception.with_traceback())
            logging.error("An error has occured.")

    def run(self, command: str, shell) -> CmdResult:
        """Run a command inside the SSH server."""
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
        except paramiko.SSHException as exception:
            logging.debug(exception.with_traceback())
            logging.error(exception)
        else:
            return stdin, stdout, stderr
