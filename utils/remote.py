class CmdResult:
    def __init__(self, stdout, stderr, exit_code):
        self.sdtout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    def print_cmd(self):
        for line in self.sdtout.read().splitlines():
            print(line.decode("utf-8"))
