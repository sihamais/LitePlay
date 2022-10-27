from utils import SSH
from . import BaseModule


class AptModule(BaseModule):
    name: str = "apt"

    def process(self, ssh_client: SSH):
        """Apply the action to `ssh_client` using `params`."""
