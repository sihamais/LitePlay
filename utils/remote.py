from . import SSH


def run_cmd(command: str, ssh_client: SSH, config: dict) -> CmdResult:
    """Execute the `command` remotely using the `SSHClient`.

    The `CmdResult` object will expose the following information:
    - `CmdResult.stdout`: the standard output of the `command` execution
    - `CmdResult.stderr`: the error output of the `command` execution
    - `CmdResult.exit_code`: the exit code of the `command` execution
    """
    stdin, stdout, stderr = ssh_client.run(command, shell)
