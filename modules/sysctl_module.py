from utils.ssh import SSHClient
from utils.cmd_result import CmdResult
from utils.status import Status
from modules.base_module import BaseModule
import logging


class SysctlModule(BaseModule):
    name: str = "sysctl"

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s attribute=%s value=%s permanent=%s",
            self.task_number,
            self.host,
            self.name,
            self.params["attribute"],
            self.params["value"],
            self.params["permanent"],
        )

    def _diff(self, ssh_client: SSHClient):
        """Check the difference between the actual state of the server and the changes to be applied."""
        if self.params["permanent"]:
            check = f'sysctl --system | grep -E "(^| ){self.params["attribute"]}( |$)" | rev | cut -d" " -f 1 | rev'
            result: CmdResult = ssh_client.run(check)

            if result.stdout().__contains__(str(self.params["value"])):
                self.status = Status.OK
                return
            else:
                self.status = Status.CHANGED
                return f'echo {self.params["attribute"]}={self.params["value"]} > /etc/sysctl.d/{self.params["attribute"]}-sysctl.conf'
        else:
            check = f'sysctl -n {self.params["attribute"]}'
            result: CmdResult = ssh_client.run(check)

            if result.stdout() == self.params["value"]:
                self.status = Status.OK
                return
            else:
                self.status = Status.CHANGED
                return (
                    f'sysctl -w {self.params["attribute"]}={self.params["value"]}'
                )
