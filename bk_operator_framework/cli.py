import click

from bk_operator_framework._cli_actions import init as cli_actions_init
from bk_operator_framework._cli_actions import version as cli_actions_version


@click.group(name="bof", epilog='Use "bof [command] --help" for more information about a command.')
def bof() -> None:
    """CLI tool for building Kubernetes extensions and tools."""
    pass


@bof.command()
def init():
    """Initialize a new bof project."""
    cli_actions_init.main()


@bof.command()
def create():
    """Create a new bof component."""
    click.echo("Creation complete.")


@bof.command()
def edit():
    """Edit the bof project configuration."""
    click.echo("Edit complete.")


@bof.command()
def version():
    """Print the bof version."""
    cli_actions_version.main()


if __name__ == "__main__":
    bof(prog_name="bof")
