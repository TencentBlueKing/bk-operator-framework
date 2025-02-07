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

import os
import sys

import kopf

from bk_operator_framework.constants import ServerType
from bk_operator_framework.kits.env import (
    load_auth_and_cluster_info,
    running_in_cluster,
)
from bk_operator_framework.kits.module import load_server_modules


def _configure_admission_server() -> None:
    """
    Configure Kopf Admission Server
    :return:
    """

    @kopf.on.startup()
    def configure(settings: kopf.OperatorSettings, **_):
        # Assuming that the configuration is done manually:
        if running_in_cluster():
            webhook_kwargs = {
                "port": int(os.getenv("WEBHOOK_PORT", 8443)),
                "certfile": os.getenv("WEBHOOK_TLS_CERT_PATH", "/workspace/etc/certs/tls.crt"),
                "pkeyfile": os.getenv("WEBHOOK_TLS_KEY_PATH", "/workspace/etc/certs/tls.key"),
            }
        else:
            webhook_kwargs = {
                "port": int(os.getenv("WEBHOOK_PORT", 8443)),
            }
        settings.admission.server = kopf.WebhookServer(**webhook_kwargs)


def prepare_startup() -> None:
    """
    Some preparations before starting kopf
    :return:
    """
    load_auth_and_cluster_info()

    server_type = sys.argv.pop(2)
    load_server_modules(server_type)
    if server_type == ServerType.Webhook.value:
        _configure_admission_server()
