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
