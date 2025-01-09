import sys

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template
from bk_operator_framework.core.project import project_desc


def main(domain: str) -> None:
    echo.info("Writing scaffold for you to edit...")
    if project_desc.is_initialized:
        echo.fata("Failed to initialize project: already initialized")
        echo.info("Next: define a resource with:\n$ bof create api")
        sys.exit(1)

    template.init_project_dir()
    project_desc.init_basc_info(domain)

    echo.info("Project initialization completed!")
    echo.info("Update dependencies:\n$ pip install -r requirements.txt")
    echo.info("Next: define a resource with:\n$ bof create api")
