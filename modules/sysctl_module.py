from utils.ssh import SSHClient
from . import BaseModule

# read valeur: sysctl -n dev.raid.speed_limit_max -> 2000
# set valeur: sysctl dev.raid.speed_limit_max=300


class SysctlModule(BaseModule):
    name: str = "sysctl"

    valueInfo: dict = {
        "check": "-n",
        "action": "=",
    }

    def apply(self, ssh_client: SSHClient):
        """Apply the action to `ssh_client` using `params`."""
        command, status = self.diff(ssh_client)
        if status is Status.CHANGED:
            ssh_client.run(command)
            logging.info("[%d][CHANGED] %s", self.task_number, command)
        else:
            logging.info(
                "[%d][OK] Sysctl %s %s",
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
                "[%d][OK] Sysctl %s %s %s",
                self.task_number,
                self.params["attribute"],
                self.valueInfo["action"],
                self.params["value"],
            )

    def diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""
        status: str

        check = f'sudo sysctl {self.stateInfo["check"]} {self.params["attribute"]}'
        result: CmdResult = ssh_client.run(check)

        if result.stdout.read() == self.params["value"]:
            status = Status.OK
        else:
            status = Status.CHANGED

        cmd = f'sudo sysctl {self.params["attribute"]}{self.stateInfo["action"]}{self.params["value"]}'
        return cmd, status
