from utils.ssh import SSHClient
from utils.cmd_result import CmdResult
from modules.base_module import BaseModule
import logging
import uuid
from jinja2 import Template


class TemplateModule(BaseModule):
    name: str = "template"

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s src=%s dest=%s",
            self.task_number,
            self.host,
            self.params["src"],
            self.params["dest"],
        )

    def apply(self, ssh_client) -> None:
        self._info()
        self._diff()
        if self.status is Status.CHANGED:
            self._process(ssh_client, command)
        self._status()

    def dry(self, ssh_client: SSHClient):
        """Display the action that would be applied to `ssh_client`."""

    def _diff(self, ssh_client: SSHClient) -> str:
        """Check the difference between the actual state of the server and the changes to be applied."""
        check = f"sudo cat {self.params['dest']}"
        result: CmdResult = ssh_client.run(check)

        file: str = open(self.params["src"], "r")
        tmpl = Template(file)
        rtmpl = tmpl.render(self.params["vars"])

        if result.stdout.read().decode("utf-8") == rtmpl:
            self.status = Status.OK
        else:
            self.status = Status.CHANGED
            # Create random temporary file
            self.rendered_file_path = f"/tmp/rendered-{uuid.uuid1()}.txt"

            with open(self.rendered_file_path, "w", encoding="utf-8") as f:
                f.write(rtmpl)  # Write template to file

    def _process(self, ssh_client, command):
        """Process the action applied to `ssh_client`."""
        sftp_client = ssh_client.session.open_sftp()
        sftp_client.put(self.rendered_file_path, self.params["dest"])
        sftp_client.close()
