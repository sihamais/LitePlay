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

    def _diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""
        if self.params["permanent"] == True:
            check = f'sysctl --system | grep {self.params["attribute"]} | rev | cut -d " " -f 1 | rev' # not good
            result: CmdResult = ssh_client.run(check)

            print(result.stdout.read().decode("utf-8"))
            if result.stdout.read().decode("utf-8") == self.params["value"]:
                self.status = Status.OK
            else:
                self.status = Status.CHANGED
                return f'sudo echo {self.params["attribute"]}={self.params["value"]} > /etc/sysctl.d/{self.params["attribute"]}-sysctl.conf'
        else:
            check = f'sudo sysctl -n {self.params["attribute"]}'
            result: CmdResult = ssh_client.run(check)


            if result.stdout.read().decode("utf-8") == self.params["value"]:
                self.status = Status.OK
            else:
                self.status = Status.CHANGED
                return (
                    f'sudo sysctl -w {self.params["attribute"]}={self.params["value"]}'
                )

    # def _diff(self, ssh_client: SSHClient) -> str:
    #     """Check the difference between the actual state of the server and the changes to be applied."""
    #     # Check if attribute is set permanently
    #     check = f'sysctl --system | grep {self.params["attribute"]} | rev | cut -d " " -f 1 | rev'
    #     result: CmdResult = ssh_client.run(check)

    #     if self.params["permanent"] == True:  # If we want it to be permanent
    #         if result.stdout.read() == self.params["value"]:
    #             self.status = Status.OK
    #         else:
    #             self.status = Status.CHANGED
    #             return f'sudo echo {self.params["attribute"]}={self.params["value"]} > /etc/sysctl.d/{self.params["attribute"]}-sysctl.conf'
    #     else:  # If we don't want it to be permanent
    #         # If attribute is set permanently
    #         if result.stdout.read() == self.params["value"]:
    #             self.status = Status.CHANGED
    #             return f"sed -i '/{self.params['attribute']}/d' /etc/sysctl.d/{self.params['attribute']}-sysctl.conf && sudo sysctl -w {self.params['attribute']}={self.params['value']}"
    #         else:
    #             self.status = Status.OK
    #             check = f'sudo sysctl -n {self.params["attribute"]}'
    #             result: CmdResult = ssh_client.run(check)

    #             if result.stdout.read() == self.params["value"]:
    #                 # If value is set (not permanently)
    #                 self.status = Status.OK
    #             else:
    #                 self.status = Status.CHANGED
    #                 return f'sudo sysctl -w {self.params["attribute"]}={self.params["value"]}'
