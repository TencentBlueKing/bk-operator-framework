import click

from bk_operator_framework._cli_actions.constant import CliText

__version__ = "1.0.0"


def main():
    click.echo(f"{CliText.INFO} bof version is {__version__}")
