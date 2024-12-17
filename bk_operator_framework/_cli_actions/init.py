import os
import shutil

import click

from bk_operator_framework._cli_actions.constant import CliText


def main():
    click.echo(f"{CliText.INFO} Initializing project structure...")
    template_dir = os.path.join(os.path.dirname(__file__), "templates", "init")
    current_dir = os.getcwd()

    api_dir = os.path.join(current_dir, "api")
    internal_dir = os.path.join(current_dir, "internal")

    if os.path.exists(api_dir) and os.path.exists(internal_dir):
        click.echo(f"{CliText.FATA} Failed to initialize project: already initialized")
        return

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(current_dir, os.path.relpath(src_file, template_dir))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)

    click.echo(f"{CliText.INFO} Project initialization completed!")
    click.echo(f"{CliText.INFO} Update dependencies:\n$ pip install -r requirements.txt")
    click.echo(f"{CliText.INFO} Next: define a resource with:\n$ bof create api")
