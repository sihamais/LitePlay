from utils.ssh import SSHClient
from utils.cmd_result import CmdResult
from modules.base_module import BaseModule
import logging

# read valeur: sysctl -n dev.raid.speed_limit_max -> 2000
# set valeur: sysctl dev.raid.speed_limit_max=300
# sysctl --system | grep x | rev | cut -d " " -f 1 | rev


class SysctlModule(BaseModule):
    name: str = "sysctl"

    valueInfo: dict = {
        "check": "-n",
        "action": "=",
    }

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s name=%s attribute=%s value=%s permanent=%s",
            self.task_number,
            self.host,
            self.name,
            self.params["attribute"],
            self.params["value"],
            self.params["permanent"],
        )

    def _diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""
        check = f'sudo sysctl {self.stateInfo["check"]} {self.params["attribute"]}'
        result: CmdResult = ssh_client.run(check)

        if result.stdout.read() == self.params["value"]:
            self.status = Status.OK
        else:
            self.status = Status.CHANGED

        return f'sudo sysctl {self.params["attribute"]}{self.stateInfo["action"]}{self.params["value"]}'
