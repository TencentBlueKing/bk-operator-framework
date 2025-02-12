"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import sys
from importlib import import_module

import kopf
from kopf._cogs.structs.references import Resource
from kopf._cogs.structs.reviews import WebhookClientConfig
from kopf._core.engines.admission import build_webhooks
from kopf._core.intents import registries

from bk_operator_framework.generator.project import Project
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


def list_project_webhooks(project: Project) -> ([], []):
    _mock_webhook_server()
    registry = registries.get_default_registry()
    all_handlers = registry._webhooks.get_all_handlers()
    mutating_handlers = [h for h in all_handlers if h.reason == "mutating"]

    webhook_resources = [
        Resource(plural=r.plural, group=f"{r.group}.{r.domain}".rstrip("."), version=r.version)
        for r in project.resources
    ]
    mutating_webhooks = build_webhooks(
        mutating_handlers,
        resources=webhook_resources,
        name_suffix=f"{project.project_name}.{project.domain}",
        client_config=WebhookClientConfig(url="", service=None),
        persistent_only=False,
    )

    validating_handlers = [h for h in all_handlers if h.reason == "validating"]

    validating_webhooks = build_webhooks(
        validating_handlers,
        resources=webhook_resources,
        name_suffix=f"{project.project_name}.{project.domain}",
        client_config=WebhookClientConfig(url="", service=None),
        persistent_only=False,
    )

    return validating_webhooks, mutating_webhooks
