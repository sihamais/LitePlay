import click
import logging
import Utils

loggingFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@click.command()
@click.option("-f", required=True, type=click.File("rb"))
@click.option("-i", required=True, type=click.File("rb"))
@click.option("--dry-run", is_flag=True)
@click.option("--debug", is_flag=True)
def cli(f, i, dry_run, debug):
    if debug:
        loggingLevel = logging.DEBUG
    else:
        loggingLevel = logging.INFO

    logging.basicConfig(format=loggingFormat, level=loggingLevel)

    todos = Utils.YamlHandler.read(f)
    inventory = Utils.YamlHandler.read(i)

    ssh_addresses = []
    for key in inventory["hosts"]:
        ssh_addresses.append(inventory["hosts"][key]["ssh_address"])

    logging.info("processing %d tasks on hosts: %s",
                 len(todos), " ".join(ssh_addresses))
