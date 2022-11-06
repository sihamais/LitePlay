from utils.ssh import SSHClient
from utils.cmd_result import CmdResult
from modules.base_module import BaseModule
from utils.status import Status
import logging


class ServiceModule(BaseModule):
    name: str = "service"

    stateInfo: dict = {
        "started": {
            "check": "is-active",
            "expected": "active",
            "opposite": "stopped",
            "action": "start",
        },
        "stopped": {
            "check": "is-active",
            "expected": "inactive",
            "opposite": "stopped",
            "action": "stop",
        },
        "enabled": {
            "check": "is-enabled",
            "expected": "enabled",
            "opposite": "stopped",
            "action": "enable",
        },
        "disabled": {
            "check": "is-enabled",
            "expected": "disabled",
            "opposite": "stopped",
            "action": "disable",
        },
        "restarted": {"action": "restart"},
    }

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
        result: CmdResult = self._exists(ssh_client)  # Check if the service exists

        if result.exit_code != 0:  # If the service doesn't exist
            self.status = Status.KO
            result.log_stdout(logging.debug, self.task_number)
            return
        else:  # If the service exist
            if self.params["state"] == "restarted":
                self.status = Status.CHANGED
            else:
                check = f'sudo systemctl {self.stateInfo[self.params["state"]]["check"]} {self.params["name"]}.service'  # Commmand to check the state of the service (idempotence)
                result: CmdResult = ssh_client.run(check)

                if (
                    result.stdout.read().decode("utf-8")
                    == self.stateInfo[self.params["state"]]["expected"]
                ):
                    self.status = Status.OK
                else:
                    self.status = Status.CHANGED

            cmd = f'sudo systemctl {self.stateInfo[self.params["state"]]["action"]} {self.params["name"]}.service'  # Command to execute the action
            return cmd

    def _exists(self, ssh_client: SSHClient):
        """Check if the service exists on the host."""
        command = f'sudo systemctl list-unit-files {self.params["name"]}.service'
        return ssh_client.run(command)
