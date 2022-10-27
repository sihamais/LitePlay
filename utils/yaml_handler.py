import yaml
import logging
import click


def read(file: click.File()):
    """Read YAML file content and returns it."""
    try:
        data = yaml.safe_load(file)
    except yaml.YAMLError as exception:
        logging.debug(exception.with_traceback())
        logging.error("An error occured.")
    else:
        return data
