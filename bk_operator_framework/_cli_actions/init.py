import os
import shutil

import click


def main():
    template_dir = os.path.join(os.path.dirname(__file__), "templates", "init")
    current_dir = os.getcwd()

    api_dir = os.path.join(current_dir, "api")
    internal_dir = os.path.join(current_dir, "internal")

    if os.path.exists(api_dir) and os.path.exists(internal_dir):
        fata_text = click.style("FATA", fg="red")
        error_message = f"{fata_text} Failed to initialize project: already initialized"
        click.echo(error_message)
        return

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(current_dir, os.path.relpath(src_file, template_dir))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)

    success_text = click.style("INFO", fg="green")
    click.echo(f"{success_text} Project initialization completed!")
