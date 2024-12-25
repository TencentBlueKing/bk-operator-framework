from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template
from bk_operator_framework.core.project import project_desc


def main(group, version, kind, plural, namespaced, controller, resource):
    echo.info("Writing scaffold for you to edit...")

    singular = kind.lower()
    if not plural:
        plural = f"{singular}s"

    project_desc.reload()

    if resource:
        template.create_resource(group, version, kind, singular, plural, project_desc.domain)

    if controller:
        template.create_controller(group, version, kind, singular, plural)

    if resource or controller:
        project_desc.create_or_update_resources(
            group, version, kind, plural, singular, resource, controller, namespaced
        )
        project_desc.render()
