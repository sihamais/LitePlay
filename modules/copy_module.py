from utils.ssh import SSHClient
from . import BaseModule
from datetime import datetime
import os


class CopyModule(BaseModule):
    name: str = "copy"

    def apply(self, ssh_client: SSHClient):
        # backup mode, set a timestamp if backup is set to true
        if self.params["backup"]:
            now = datetime.now()
            ssh_client.run(f'mv {self.params["dest"]} {self.params["dest"]}_{now}')

        sftp_client = ssh_client.session.open_sftp()
        upload_dir(self.params["src"], self.params["dest"], sftp_client)
        sftp_client.close()

    def upload_dir(src, dest, sftp_client):
        for file in os.listdir(src):
            if os.path.isdir(f"{src}/{file}"):
                try:
                    sftp_client.chdir(f"{dest}/{file}")  # Test if folder exist
                except IOError:
                    sftp_client.mkdir(f"{dest}/{file}")  # Create new folder
                    sftp_client.chdir(f"{dest}/{file}")
                upload_dir(f"{src}/{file}", f"{dest}/{file}", sftp_client)
            else:
                sftp_client.put(f"{src}/{file}", f"{dest}/{file}")
