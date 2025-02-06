import sys
from importlib import import_module

import kopf
from kopf._cogs.structs.references import Resource
from kopf._cogs.structs.reviews import WebhookClientConfig
from kopf._core.engines.admission import build_webhooks
from kopf._core.intents import registries

from bk_operator_framework.kits.module import list_all_modules


def _mock_webhook_server() -> None:
    module = import_module("internal.webhook")
    module_dir = module.__path__[0]
    sys.path_importer_cache.pop(module_dir, None)
    modules = list_all_modules(module_dir)
    for name in modules:
        module_path = "{}.{}".format(module.__name__, name)
        import_module(module_path)

    @kopf.on.startup()
    def configure(settings: kopf.OperatorSettings, **_):
        settings.admission.server = kopf.WebhookServer()


def list_project_webhooks(project_name: str, domain: str, project_desc: str) -> None:
    _mock_webhook_server()
    registry = registries.get_default_registry()
    all_handlers = registry._webhooks.get_all_handlers()
    mutating_handlers = [h for h in all_handlers if h.reason == "mutating"]

    webhook_resources = [
        Resource(plural=r.plural, group=f"{r.group}.{r.domain}".rstrip("."), version=r.version)
        for r in project_desc.resources
    ]
    mutating_webhooks = build_webhooks(
        mutating_handlers,
        resources=webhook_resources,
        name_suffix=f"{project_name}.{domain}",
        client_config=WebhookClientConfig(url=None, service=None),
        persistent_only=False,
    )

    validating_handlers = [h for h in all_handlers if h.reason == "validating"]

    validating_webhooks = build_webhooks(
        validating_handlers,
        resources=webhook_resources,
        name_suffix=f"{project_name}.{domain}",
        client_config=WebhookClientConfig(url=None, service=None),
        persistent_only=False,
    )

    return validating_webhooks, mutating_webhooks
