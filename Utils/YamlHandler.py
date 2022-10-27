import yaml
import logging


def read(file):
    try:
        return yaml.safe_load(file)
    except yaml.YAMLError as exception:
        logging.debug(exception)
        logging.error("An error occured.")
