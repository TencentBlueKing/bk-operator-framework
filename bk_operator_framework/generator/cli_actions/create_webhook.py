import sys

from bk_operator_framework.generator.cli_actions import echo
from bk_operator_framework.generator.kits import template
from bk_operator_framework.generator.project import project


def main(
    group: str, version: str, kind: str, plural: str, defaulting: bool, validation: bool, external_api_domain: str
):
    if not defaulting and not validation:
        echo.fata("bof create webhook requires at least one of --defaulting and --validation to be true ")
        sys.exit(1)

    webhooks = {"defaulting": defaulting, "validation": validation}

    project.reload_with_desc_file()
    desire_resource = project.create_or_update_resource(
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
    project.render_desc_file()
