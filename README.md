# LitePlay

Minimalist Ansible copycat.

## Usage

```
$ liteplay -f tests/playbook.yml -i tests/inventory.yml
```

## Options

| Flag    | Description                                           |
| ------- | ----------------------------------------------------- |
| dry-run | **[Optional]** Validate the playbook before execution |
| debug   | **[Optional]** Shows excecution errors                |

## Modules

| Module   | Description                          |
| -------- | ------------------------------------ |
| apt      | Manage apt packages                  |
| command  | Execute bash command                 |
| copy     | Copy files on remote host            |
| service  | Manage systemctl services            |
| sysctl   | Manage sysctl configuration          |
| template | Render jinja template on remote host |
