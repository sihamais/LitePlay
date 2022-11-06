from utils.ssh import SSHClient, CmdResult
from utils.status import Status
from modules.base_module import BaseModule
import logging


class AptModule(BaseModule):
    name: str = "apt"

    stateInfo: dict = {
        "present": {"expected": 0, "action": "install"},
        "absent": {"expected": 1, "action": "remove"},
    }

    def __init__(self, params: dict, task_number: int, host: str):
        if params["state"] is None:
            params["state"] = "present"
        super().__init__(params, task_number, host)

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s name=%s state=%s",
            self.task_number,
            self.host,
            self.name,
            self.params["name"],
            self.params["state"],
        )

    def _diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""

        check = f"sudo dpkg -s {self.params['name']}"
        result: CmdResult = ssh_client.run(check)

        if result.exit_code == self.stateInfo[self.params["state"]]["expected"]:
            self.status = Status.OK
        else:
            self.status = Status.CHANGED

        return f"sudo apt -y {self.stateInfo[self.params['state']]['action']} {self.params['name']}"

