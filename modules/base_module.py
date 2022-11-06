from ssh.ssh_client import SSHClient


class BaseModule:
    name: str = "anonymous"
    task_number: int = -1

    def __init__(self, params: dict, task_number: int):
        self.params = params
        self.task_number = task_number

    def apply(self, ssh_client: SSHClient):
        """Apply the action to `ssh_client` using `params`."""

    def diff(self, ssh_client: SSHClient):
        """Get changes to be applied."""
