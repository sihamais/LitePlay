import yaml
import logging
import click


def read(file: click.File()) -> Any:
    """Read YAML file content and returns it."""
    try:
        data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as exception:
        logging.debug(exception.with_traceback())
        logging.error("An error occured.")
