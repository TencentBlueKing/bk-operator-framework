from kopf._cogs.structs.references import Resource
from kopf._cogs.structs.reviews import WebhookClientConfig
from kopf._core.engines.admission import build_webhooks
from kopf._core.intents import registries

from bk_operator_framework.core.runtime import load_server


def get_webhooks(project_name, domain, project_desc):
    load_server("webhook")
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
