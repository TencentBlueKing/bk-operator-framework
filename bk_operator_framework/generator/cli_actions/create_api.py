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
