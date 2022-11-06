from utils.ssh import SSHClient
from utils.ssh import CmdResult
from . import BaseModule


class AptModule(BaseModule):
    name: str = "apt"

    stateInfo: dict = {
        "present": {"expected": 0, "action": "install"},
        "absent": {"expected": 1, "action": "remove --purge"},
    }

    def __init__(self, params: dict, task_number: int):
        if params["state"] is None:
            params["state"] = "present"
        super().__init__(params, task_number)

    def apply(self, ssh_client: SSHClient):
        command, status = self.diff(ssh_client)
        if status is Status.CHANGED:
            ssh_client.run(command)
            logging.info("[%d][CHANGED] %s", self.task_number, command)
        else:
            logging.info(
                "[%d][OK] Package %s %s",
                self.task_number,
                self.params["name"],
                self.params["state"],
            )

    def dry(self, ssh_client: SSHClient):
        """Display the action that would be applied to `ssh_client`."""
        command, status = self.diff(ssh_client)
        if status is Status.CHANGED:
            logging.info("[%d][CHANGED] %s", self.task_number, command)
        else:
            logging.info(
                "[%d][OK] Package %s %s",
                self.task_number,
                self.params["name"],
                self.params["state"],
            )

    def diff(self, ssh_client: SSHClient) -> (str, str):
        """Check the difference between the actual state of the server and the changes to be applied."""
        status: str

        check = f"dpkg -l {self.params['name']}"
        result: CmdResult = ssh_client.run(check, ssh_client)

        if result.exit_code == self.stateInfo[self.params["state"]]["expected"]:
            status = Status.OK
        else:
            status = Status.CHANGED

        cmd = f"sudo apt-get -y {self.stateInfo[self.params['state']]['action']}"
        return cmd, status
