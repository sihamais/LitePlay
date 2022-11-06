from utils.ssh import SSHClient
from utils.cmd_result import CmdResult
from modules.base_module import BaseModule
from datetime import datetime
import os
import logging

# check: test -e file OU test -d file (directory)
# $ ssh user@remote-host "cat /home/root/file_remote" | diff  - file_local 
class CopyModule(BaseModule):
    name: str = "copy"

    def apply(self, ssh_client: SSHClient):
        # backup mode, set a timestamp if backup is set to true
        if self.params["backup"]:
            now = datetime.now()
            ssh_client.run(f'mv {self.params["dest"]} {self.params["dest"]}_{now}')

        sftp_client = ssh_client.session.open_sftp()
        self.upload_dir(self.params["src"], self.params["dest"], sftp_client)
        sftp_client.close()

    def dry(self, ssh_client: SSHClient):
        """Display the action that would be applied to `ssh_client`."""
        command, status = self.diff(ssh_client)
        if status is Status.CHANGED:
            logging.info("[%d][CHANGED] %s", self.task_number, command)
        else:
            logging.info(
                "[%d][OK] %s %s %s",
                self.task_number,
                self.name,
                self.params["name"],
                self.params["state"],
            )

    def diff(self, ssh_client: SSHClient):
        pass

    def upload_dir(self, src, dest, sftp_client):
        for file in os.listdir(src):
            if os.path.isdir(f"{src}/{file}"):
                try:
                    sftp_client.chdir(f"{dest}/{file}")  # Test if folder exist
                except IOError:
                    sftp_client.mkdir(f"{dest}/{file}")  # Create new folder
                    sftp_client.chdir(f"{dest}/{file}")
                self.upload_dir(f"{src}/{file}", f"{dest}/{file}", sftp_client)
            else:
                sftp_client.put(f"{src}/{file}", f"{dest}/{file}")
