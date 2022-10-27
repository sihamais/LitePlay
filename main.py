import click
import logging
import utils

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
