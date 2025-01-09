import sys

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template
from bk_operator_framework.core.project import project_desc


def main(
    group: str,
    version: str,
    kind: str,
    plural: str,
    namespaced: str,
    controller: bool,
    resource: bool,
    external_api_domain: str,
) -> None:
    if resource and external_api_domain is not None:
        echo.fata(
            "Cannot use '--external-api-domain' when creating an API in the project with '--resource=true'. Use '--resource=false' when referencing an external API. "
        )
        sys.exit(1)

    desire_resource = project_desc.create_or_update_resource(
        group,
        version,
        kind,
        plural=plural,
        resource=resource,
        controller=controller,
        namespaced=namespaced,
        external_api_domain=external_api_domain,
    )

    echo.info("Writing scaffold for you to edit...")
    if resource:
        template.create_resource_api(group, version, kind, desire_resource.singular, plural, desire_resource.domain)
    if controller:
        template.create_resource_controller(
            group, version, kind, desire_resource.singular, desire_resource.plural, external_api_domain
        )

    project_desc.render()
