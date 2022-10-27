from utils import SSH
from utils import remote
from . import BaseModule


class CommandModule(BaseModule):
    name: str = "command"

    def process(self, ssh_client: SSH):
        """Apply the action to `ssh_client` using `params`."""
        remote.run_cmd(command, ssh_client, config)
