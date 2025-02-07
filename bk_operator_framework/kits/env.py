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

from kubernetes import config


def running_in_cluster() -> bool:
    """
    Is the current operating environment in the k8s cluster?
    :return:
    """
    return "KUBERNETES_SERVICE_HOST" in os.environ


def load_auth_and_cluster_info() -> None:
    """
    Loads authentication and cluster information
    :return:
    """
    if running_in_cluster():
        config.load_incluster_config()
    else:
        config.load_kube_config()
