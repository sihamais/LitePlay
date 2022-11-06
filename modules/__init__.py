from apt_module import AptModule
from base_module import BaseModule
from command_module import CommandModule
from copy_module import CopyModule
from service_module import ServiceModule
from sysctl_module import SysctlModule
from template_module import TemplateModule
from enum import Enum


class Status(Enum):
    OK = "OK"
    KO = "KO"
    CHANGED = "CHANGED"
