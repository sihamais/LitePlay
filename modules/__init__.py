from apt import AptModule
from base import BaseModule
from command import CommandModule
from copy import CopyModule
from service import ServiceModule
from sysctl import SysctlModule
from template import TemplateModule
from enum import Enum


class Status(Enum):
    OK = "OK"
    KO = "KO"
    CHANGED = "CHANGED"
