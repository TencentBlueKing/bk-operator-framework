import sys

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core.project import project_desc


def main(group, version, kind, plural, defaulting, validation):
    if not defaulting and not validation:
        echo.fata("bof create webhook requires at least one of --defaulting and --validation to be true ")
        sys.exit(1)

    echo.info("Writing scaffold for you to edit...")

    singular = kind.lower()
    if not plural:
        plural = f"{singular}s"

    webhook_target_resource = f"{plural}.{group}.{project_desc.domain}/{version}"

    project_desc.reload()
    for resource in project_desc.resources:
        current_resource = f"{resource.plural}.{resource.group}.{resource.domain}/{version}"
        if current_resource == webhook_target_resource:
            current_resource.webhooks = ""
    sys.exit(1)
