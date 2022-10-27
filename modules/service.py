from ssh.ssh_client import SSHClient
from . import BaseModule
from . import Status
from utils import remote
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

    def process(self, ssh_client):
        """Apply the action to `ssh_client` using `params`."""
        command, status = self.diff(ssh_client)
        if status is Status.CHANGED:
            remote.run_cmd(command, ssh_client)
            logging.info("[%d][CHANGED] %s", self.task_number, command)
        else:
            logging.info(
                "[%d][OK] Service %s %s",
                self.task_number,
                self.params["name"],
                self.params["state"],
            )

    def dry(self, ssh_client):
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

    def diff(self, ssh_client) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""
        status: str

        if self.params["state"] == "restarted":
            status = Status.CHANGED
        else:
            check = str.format(
                "sudo systemctl %s %s.service",
                stateInfo[self.params["state"]]["check"],
                self.params["name"],
            )
            output = remote.run_cmd(check, ssh_client)

            if output == stateInfo[self.params["state"]]["expected"]:
                status = Status.OK
            else:
                status = Status.CHANGED

        cmd = str.format(
            "sudo systemctl %s %s.service",
            stateInfo[self.params["state"]]["action"],
            self.params["name"],
        )
        return cmd, status
