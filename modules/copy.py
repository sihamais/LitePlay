from ssh.ssh_client import SSHClient
from . import BaseModule


class CopyModule(BaseModule):
    name: str = "copy"

    def process(self, ssh_client):
        """Apply the action to `ssh_client` using `params`."""
