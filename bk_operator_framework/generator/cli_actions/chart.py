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

from importlib import import_module

from bk_operator_framework.generator.cli_actions import echo
from bk_operator_framework.generator.kits import template
from bk_operator_framework.generator.kits.schema import get_openapi_v3_schema
from bk_operator_framework.generator.kits.webhook import list_project_webhooks
from bk_operator_framework.generator.project import project


def main(part):
    echo.info("Writing scaffold for you to edit...")

    project.reload_with_desc_file()
    project.create_or_update_chart(part)

    template.create_or_update_chart_basic_file(project.project_name, project.chart.version, project.chart.appVersion)

    resource_versions_dict = {}
    cluster_role_rule_list = []
    exist_controller = False
    exist_webhook = False
    for resource in project.resources:
        if resource.api:
            key = f"{resource.plural}.{resource.group}.{resource.domain}"
            resource_versions_dict.setdefault(key, [])
            resource_schema_module = import_module(
                f"api.{resource.group}.{resource.version}.{resource.singular}_schemas"
            )
            resource_schema_model = getattr(resource_schema_module, resource.kind)
            resource_additional_printer_columns = getattr(resource_schema_module, "ADDITIONAL_PRINTER_COLUMN_LIST")
            openapi_v3_schema = get_openapi_v3_schema(resource_schema_model)
            if not openapi_v3_schema.get("properties", {}).get("status", {}).get("properties"):
                openapi_v3_schema["properties"].pop("status", None)
            resource_versions_dict[key].append(
                {
                    "resource": resource,
                    "openapi_v3_schema": openapi_v3_schema,
                    "additional_printer_columns": resource_additional_printer_columns,
                }
            )
        if resource.controller:
            controller_module = import_module(f"internal.controller.{resource.singular}_controller")
            cluster_role_rule_list.extend(getattr(controller_module, "RBAC_RULE_LIST"))
            exist_controller = True
        if resource.webhooks:
            exist_webhook = True

    for _, resource_versions in resource_versions_dict.items():
        template.create_or_update_chart_crds(resource_versions)

    validating_webhooks, mutating_webhooks = [], []
    if exist_webhook:
        validating_webhooks, mutating_webhooks = list_project_webhooks(project.project_name, project.domain, project)

    template.create_or_update_chart_templates(
        project.project_name,
        cluster_role_rule_list,
        validating_webhooks,
        mutating_webhooks,
        exist_controller,
        exist_webhook,
    )

    template.create_chart_values(project.project_name, exist_controller, exist_webhook)
