from ssh.ssh_client import SSHClient


class BaseModule:
    name: str = "anonymous"

    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client: SSHClient):
        """Apply the action to `ssh_client` using `params`."""

    def diff(self, ssh_client):
        """Get changes to be applied."""
