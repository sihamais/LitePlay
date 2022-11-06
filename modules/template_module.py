from ssh.ssh_client import SSHClient
from . import BaseModule
from jinja2 import Template


class TemplateModule(BaseModule):
    name: str = "template"

    def apply(self, ssh_client) -> None:
        file: str = open(self.params["src"], "r")
        tmp = Template(file)
        print(tmp)
