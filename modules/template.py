from ssh.ssh_client import SSHClient
from . import BaseModule


class TemplateModule(BaseModule):
    name: str = "template"

    def process(self, ssh_client):
        """Apply the action to `ssh_client` using `params`."""
