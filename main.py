import click
import logging
import utils
from utils.status import Status
from modules.apt_module import AptModule
from modules.command_module import CommandModule
from modules.copy_module import CopyModule
from modules.service_module import ServiceModule
from modules.sysctl_module import SysctlModule
from modules.template_module import TemplateModule

loggingFormat: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@click.command()
@click.option("-f", required=True, type=click.File("rb"))
@click.option("-i", required=True, type=click.File("rb"))
@click.option("--dry-run", is_flag=True)
@click.option("--debug", is_flag=True)
def cli(f, i, dry_run, debug):
    """Run the CLI."""

    if debug:
        loggingLevel = logging.DEBUG
    else:
        logging.getLogger("paramiko").setLevel(logging.ERROR)
        loggingLevel = logging.INFO

    logging.basicConfig(format=loggingFormat, level=loggingLevel)

    todos: dict = utils.yaml_handler.read(f)
    inventory: dict = utils.yaml_handler.read(i)

    ssh_addresses: list = []
    for key in inventory["hosts"]:
        ssh_addresses.append(inventory["hosts"][key]["ssh_address"])

    logging.info(
        "processing %d tasks on hosts: %s", len(todos), " ".join(ssh_addresses)
    )

    task_number = 1
    for key in inventory["hosts"]:
        ssh_client = utils.ssh.SSHClient(inventory["hosts"][key])
        ssh_client.authenticate()
        ssh_client.connect()

        oks = 0
        kos = 0
        changed = 0

        for todo in todos:
            params = todo["params"]
            module = todo["module"]
            host = inventory["hosts"][key]["ssh_address"]

            if module == "apt":
                module = AptModule(params, task_number, host)
            elif module == "command":
                module = CommandModule(params, task_number, host)
            elif module == "copy":
                module = CopyModule(params, task_number, host)
            elif module == "service":
                module = ServiceModule(params, task_number, host)
            elif module == "sysctl":
                module = SysctlModule(params, task_number, host)
            elif module == "template":
                module = TemplateModule(params, task_number, host)
            else:
                logging.error("Module %s not found.", module)
                break

            if dry_run:
                module.dry(ssh_client)
            else:
                module.apply(ssh_client)

            if module.status is Status.OK:
                oks += 1
            elif module.status is Status.CHANGED:
                changed += 1
            else:
                kos += 1
                
            task_number += 1

        logging.info("host=%s ok=%d changed=%d ko=%d", host, oks, kos, changed)

    logging.info("done processing tasks for hosts: %s", " ".join(ssh_addresses))
