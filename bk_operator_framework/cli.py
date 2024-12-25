import click

from bk_operator_framework.cli_actions import chart as cli_actions_chart
from bk_operator_framework.cli_actions import create_api as cli_actions_create_api
from bk_operator_framework.cli_actions import (
    create_webhook as cli_actions_create_webhook,
)
from bk_operator_framework.cli_actions import init as cli_actions_init
from bk_operator_framework.cli_actions import version as cli_actions_version
from bk_operator_framework.cli_actions.echo import CliText


@click.group(name="bof", epilog='Use "bof [command] --help" for more information about a command.')
def bof() -> None:
    """CLI tool for building Kubernetes extensions and tools."""
    pass


@bof.command()
def version():
    """Print the bof version."""
    cli_actions_version.main()


@bof.command()
@click.option("--domain", type=str, default="my.domain", help="Resource Group")
def init(domain):
    """Initialize a new bof project."""
    cli_actions_init.main(domain)


@bof.group(
    help="Scaffold a Kubernetes API or webhook.",
    epilog='Use "bof create [command] --help" for more information about a command.',
)
def create():
    """Scaffold a Kubernetes API or webhook."""
    pass


@create.command(help="Scaffold a Kubernetes API")
@click.option("--group", type=str, required=True, help="Resource Group")
@click.option("--version", type=str, required=True, help="Resource Version")
@click.option("--kind", type=str, required=True, help="Resource Kind")
@click.option("--plural", type=str, help="resource irregular plural form")
@click.option("--namespaced", type=bool, default=True, help="Resource is namespaced (default true)")
@click.option(
    "--resource",
    is_flag=True,
    prompt=f"{CliText.INFO} Create Resource",
    help="if set, generate the resource without prompting the user (default true)",
)
@click.option(
    "--controller",
    is_flag=True,
    prompt=f"{CliText.INFO} Create Controller",
    help="if set, generate the controller without prompting the user (default true)",
)
def api(group, version, kind, plural, namespaced, controller, resource):
    cli_actions_create_api.main(group, version, kind, plural, namespaced, controller, resource)


@create.command(help="Scaffold a webhook for an API resource")
def webhook():
    cli_actions_create_webhook.main()


@bof.command()
@click.option(
    "--part",
    type=click.Choice(["major", "minor", "patch"]),
    help="Helm Chart Semantic Versioning Part",
    default="patch",
)
def chart(part):
    """Generate helm chart for the project."""
    cli_actions_chart.main(part)


if __name__ == "__main__":
    bof(prog_name="bof")
