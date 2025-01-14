import sys

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template
from bk_operator_framework.core.project import project_desc


def main(
    group: str, version: str, kind: str, plural: str, defaulting: bool, validation: bool, external_api_domain: str
):
    if not defaulting and not validation:
        echo.fata("bof create webhook requires at least one of --defaulting and --validation to be true ")
        sys.exit(1)

    webhooks = {"defaulting": defaulting, "validation": validation}
    desire_resource = project_desc.create_or_update_resource(
        group, version, kind, plural=plural, external_api_domain=external_api_domain, webhooks=webhooks
    )
    echo.info("Writing scaffold for you to edit...")
    template.create_resource_webhook(
        group,
        version,
        kind,
        desire_resource.singular,
        desire_resource.plural,
        desire_resource.domain,
        defaulting,
        validation,
        external_api_domain,
        desire_resource.api,
    )
    project_desc.render()
