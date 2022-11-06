from utils.ssh import SSHClient
from utils.ssh import CmdResult
from . import BaseModule
from . import Status
import logging


class ServiceModule(BaseModule):
    name: str = "service"

    stateInfo: dict = {
        "started": {"check": "is-active", "expected": "active", "action": "start"},
        "stopped": {"check": "is-active", "expected": "inactive", "action": "stop"},
        "enabled": {"check": "is-enabled", "expected": "enabled", "action": "enable"},
        "disabled": {
            "check": "is-enabled",
            "expected": "disabled",
            "action": "disable",
        },
        "restarted": {"action": "restart"},
    }

    def apply(self, ssh_client: SSHClient):
        """Apply the action to `ssh_client` using `params`."""
        command, status = self.diff(ssh_client)
        if status is Status.CHANGED:
            ssh_client.run(command)
            logging.info("[%d][CHANGED] %s", self.task_number, command)
        else:
            logging.info(
                "[%d][OK] Service %s %s",
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
                "[%d][OK] Service %s %s",
                self.task_number,
                self.params["name"],
                self.params["state"],
            )

    def diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""
        status: str

        if self.params["state"] == "restarted":
            status = Status.CHANGED
        else:
            check = (
                f'sudo systemctl {self.stateInfo[self.params["state"]]["check"]} {self.params["name"]}.service',
            )
            result: CmdResult = ssh_client.run(check)

            if result.stdout.read() == self.stateInfo[self.params["state"]]["expected"]:
                status = Status.OK
            else:
                status = Status.CHANGED

        cmd = (
            f'sudo systemctl {self.stateInfo[self.params["state"]]["action"]} {self.params["name"]}.service',
        )
        return cmd, status
