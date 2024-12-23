import click


class CliText:
    INFO = click.style("INFO", fg="blue")
    FATA = click.style("FATA", fg="red")
    WARN = click.style("WARN", fg="yellow")


def info(message):
    click.echo(f"{CliText.INFO} {message}")


def warn(message):
    click.echo(f"{CliText.WARN} {message}")


def fata(message):
    click.echo(f"{CliText.FATA} {message}")
