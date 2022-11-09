from paramiko import SFTPClient
from utils.ssh import SSHClient
from utils.status import Status
from utils.cmd_result import CmdResult
from modules.base_module import BaseModule
from datetime import datetime
import os
import logging
import uuid
import subprocess


class CopyModule(BaseModule):
    name: str = "copy"

    def _info(self):
        """Display information on the task."""
        logging.info(
            "[%d] host=%s op=%s src=%s dest=%s backup=%s",
            self.task_number,
            self.host,
            self.name,
            self.params["src"],
            self.params["dest"],
            self.params["backup"],
        )

    def apply(self, ssh_client: SSHClient):
        """Apply the action to `ssh_client` using `params`."""
        self._info()

        command = self._diff(ssh_client)
        if self.status is Status.CHANGED:
            self._process(ssh_client)

    def dry(self, ssh_client: SSHClient):
        """Display the action that would be applied to `ssh_client`."""
        self._info()
        self._diff(ssh_client)
        self._status()

    def _diff(self, ssh_client: SSHClient):
        # if src is a directory
        if os.path.isdir(f'{self.params["src"]}'):

            # Check that the directory exists, compress dest and hash the zip
            check = f'test -d {self.params["dest"]} && find {self.params["dest"]} -type f -print0 | xargs -0 sha1sum  | cut -d " " -f 1 | sort -z | sha1sum'
            result = ssh_client.run(check)

            # If directory doesn't exist on dest
            if result.exit_code != 0:
                self.status = Status.CHANGED
            else:
                check = f'find {self.params["src"]} -type f -print0 | xargs -0 sha1sum  | cut -d " " -f 1 | sort -z | sha1sum'
                src_hash = (
                    subprocess.check_output(check, shell=True).decode("utf-8").rstrip()
                )

                if src_hash == result.stdout():
                    self.status = Status.OK
                else:
                    self.status = Status.CHANGED

        # if src is a file
        else:
            check = f"test -e {self.params['dest']} && sha1sum {self.params['dest']} | cut -d' ' -f 1"
            result = ssh_client.run(check)

            if result.exit_code != 0:
                self.status = Status().CHANGED
            else:
                check = f'sha1sum {self.params["src"]} | cut -d" " -f 1 '
                src_hash = (
                    subprocess.check_output(check, shell=True).decode("utf-8").rstrip()
                )

                if src_hash == result.stdout():
                    self.status = Status.OK
                else:
                    self.status = Status.CHANGED

    def _process(self, ssh_client):
        """Process the action applied to `ssh_client`."""
        # if src is a directory
        if os.path.isdir(f'{self.params["src"]}'):
            self._upload_dir(ssh_client)

        # if src is a file
        else:
            self._upload_file(ssh_client)

    def _upload_dir(self, ssh_client):
        sftp_client = ssh_client.session.open_sftp()

        src_tar = f"{os.path.basename(self.params['src'])}.tar.gz"
        dest_tar = f"{os.path.basename(self.params['dest'])}.tar.gz"

        # Tar the local folder
        os.system(f'tar cfz {src_tar} -C {self.params["src"]} .')

        # Before copying, backup the remote destination folder
        if self.params["backup"]:
            result: CmdResult = ssh_client.run(
                f'test -d {self.params["dest"]} && mv {self.params["dest"]} {self.params["dest"]}_backup-{uuid.uuid1()}'
            )

        # Copy local tar to remote dest
        sftp_client.put(src_tar, dest_tar)

        # Untar the remote copied file to destination
        ssh_client.run(
            f"mkdir -p {self.params['dest']} && tar -xvf {dest_tar} -C {self.params['dest']} && rm {dest_tar}"
        )
        os.remove(src_tar)

        sftp_client.close()

    def _upload_file(self, ssh_client: SSHClient):
        # backup mode, set a timestamp if backup is set to true
        if self.params["backup"]:
            folder_name = os.path.dirname(self.params["dest"])  # Get directory name
            file_name = os.path.basename(self.params["dest"])  # Get filename
            tup = os.path.splitext(file_name)  # Get name and extension from filename

            result: CmdResult = ssh_client.run(
                f'test -e {self.params["dest"]} && mv {self.params["dest"]} {folder_name}/{tup[0]}_backup-{uuid.uuid1()}{tup[1]}'
            )
            if result.exit_code != 0:
                self.status = Status.KO
                result.log_output(logging.debug, self.task_number)

        sftp_client = ssh_client.session.open_sftp()
        ssh_client.run(f"mkdir -p {os.path.dirname(self.params['dest'])}")
        sftp_client.put(self.params["src"], self.params["dest"])
        sftp_client.close()
