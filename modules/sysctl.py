from ssh.ssh_client import SSHClient
from . import BaseModule


class SysctlModule(BaseModule):
    name: str = "sysctl"

    def process(self, ssh_client):
        """Apply the action to `ssh_client` using `params`."""
