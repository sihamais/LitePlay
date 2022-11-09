from utils.ssh import SSHClient
from utils.cmd_result import CmdResult
from utils.status import Status
from modules.base_module import BaseModule
from jinja2 import Template
import logging
import uuid
import os


class TemplateModule(BaseModule):
    name: str = "template"

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s src=%s dest=%s",
            self.task_number,
            self.host,
            self.name,
            self.params["src"],
            self.params["dest"],
        )

    def _diff(self, ssh_client: SSHClient):
        """Check the difference between the actual state of the server and the changes to be applied."""
        check = f"cat {self.params['dest']}"
        result: CmdResult = ssh_client.run(check)

        file = open(self.params["src"], "r")
        content: str = "".join(file.readlines())
        tmpl = Template(content)
        rtmpl = tmpl.render(self.params["vars"])

        if result.stdout() == rtmpl:
            self.status = Status.OK
        else:
            self.status = Status.CHANGED
            folder = os.path.dirname(self.params["dest"])
            return (
                f'mkdir -p {folder} && echo "{rtmpl}" > {self.params["dest"]}'
            )
