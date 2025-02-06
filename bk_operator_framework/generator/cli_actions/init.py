import sys

from bk_operator_framework.generator.cli_actions import echo
from bk_operator_framework.generator.kits import template
from bk_operator_framework.generator.project import project


def main(domain: str) -> None:
    echo.info("Writing scaffold for you to edit...")
    if project.is_initialized:
        echo.fata("Failed to initialize project: already initialized")
        echo.info("Next: define a resource with:\n$ bof create api")
        sys.exit(1)

    template.init_project_dir()

    project.init_basc_info(domain)
    project.render_desc_file()

    echo.info("Project initialization completed!")
    echo.info("Update dependencies:\n$ pip install -r requirements.txt")
    echo.info("Next: define a resource with:\n$ bof create api")
