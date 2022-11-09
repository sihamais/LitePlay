from utils.ssh import SSHClient
from utils.status import Status
from utils.cmd_result import CmdResult
from modules.base_module import BaseModule
import logging


class CommandModule(BaseModule):
    name: str = "command"

    def __init__(self, params: dict, task_number: int, host: str):
        if "shell" not in params:
            params["shell"] = "/bin/bash"
        super().__init__(params, task_number, host)

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s cmd=%s shell=%s",
            self.task_number,
            self.host,
            self.name,
            self.params["command"],
            self.params["shell"],
        )

    def _dry_info(self, command):
        """Display information on the command to be applied in dry-run."""
        logging.info(
            "[%d] host=%s cmd='%s'",
            self.task_number,
            self.host,
            command,
        )

    def _diff(self, ssh_client: SSHClient):
        """Check the difference between the actual state of the server and the changes to be applied."""
        self.status = Status.CHANGED
        return f"{self.params['shell']} -c '{self.params['command']}'"
