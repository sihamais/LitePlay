from utils.ssh import SSHClient
from utils import remote
from . import BaseModule


class CommandModule(BaseModule):
    name: str = "command"

    def __init__(self, params: dict, task_number: int):
        if params["shell"] is None:
            params["shell"] = "/bin/bash"
        super().__init__(params, task_number)

    def apply(self, ssh_client: SSHClient):
        if self.params["shell"] != "/bin/bash":
            tmp = ssh_client.run(f"{self.params['shell']} {self.params['command']}")
        else:
            tmp = remote.run_remote_cmd(self.params["command"], ssh_client)

    def dry(self) -> None:
        """Display the action that would be applied to `ssh_client`."""
        logging.info("[%d][CHANGED] %s", self.task_number, command)

    def command(self) -> str:
        return f"{self.params['shell']} {self.params['command']}"
