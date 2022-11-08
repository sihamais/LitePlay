from utils.ssh import SSHClient
from utils.status import Status
from utils.cmd_result import CmdResult
import logging


class BaseModule:
    name: str = "anonymous"
    task_number: int = -1

    def __init__(self, params: dict, task_number: int, host: str):
        self.params = params
        self.task_number = task_number
        self.host = host

    def apply(self, ssh_client: SSHClient):
        """Apply the action to `ssh_client` using `params`."""
        self._info()

        command = self._diff(ssh_client)
        if self.status is Status.CHANGED:
            self._process(ssh_client, command)

        self._status()

    def dry(self, ssh_client: SSHClient):
        """Display the action that would be applied to `ssh_client`."""
        self._info()
        command = self._diff(ssh_client)
        if self.status is not Status.KO:
            self._dry_info(command)
        self._status()

    def _info(self):
        """Display information on the task."""

    def _status(self):
        """Display information on the status of the task."""
        logging.info(
            "[%d] host=%s op=%s status=%s",
            self.task_number,
            self.host,
            self.name,
            self.status.name,
        )

    def _dry_info(self, command):
        """Display information on the command to be applied in dry-run."""
        if self.status is Status.CHANGED:
            logging.info("[%d] host=%s cmd='%s'", self.task_number, self.host, command)

    def _diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""

    def _process(self, ssh_client, command):
        """Process the action applied to `ssh_client`."""
        result: CmdResult = ssh_client.run(command)
        if result.exit_code != 0:
            self.status = Status.KO
            result.log_stdout(logging.debug, self.task_number)
