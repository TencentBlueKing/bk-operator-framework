import sys

from bk_operator_framework.generator.cli_actions import echo
from bk_operator_framework.generator.kits import template
from bk_operator_framework.generator.project import project


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

    project.reload_with_desc_file()
    desire_resource = project.create_or_update_resource(
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
        template.create_resource_api(
            desire_resource.group,
            desire_resource.version,
            desire_resource.kind,
            desire_resource.singular,
            desire_resource.plural,
            desire_resource.domain,
        )
    if controller:
        template.create_resource_controller(
            desire_resource.group,
            desire_resource.version,
            desire_resource.kind,
            desire_resource.singular,
            desire_resource.plural,
            desire_resource.domain,
            external_api_domain,
            desire_resource.api,
        )

    project.render_desc_file()
