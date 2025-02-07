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
import pkgutil
import sys
import typing
from importlib import import_module

from bk_operator_framework.constants import ServerType
from bk_operator_framework.kits.logger import logger


def list_all_modules(module_dir: str, sub_dir: str = None) -> typing.List[str]:
    modules = []
    for _, name, is_pkg in pkgutil.iter_modules([module_dir]):
        if name.startswith("_"):
            continue
        module = name if sub_dir is None else "{}.{}".format(sub_dir, name)
        if is_pkg:
            modules += list_all_modules(os.path.join(module_dir, name), module)
        else:
            modules.append(module)
    return modules


def load_server_modules(server_type: str) -> None:
    logger.info(f"server_type is {server_type}")
    if server_type not in {ServerType.Controller.value, ServerType.Webhook.value}:
        raise RuntimeError(f"The server type[{server_type}] is invalid")
    module = import_module(f"internal.{server_type}")
    module_dir = module.__path__[0]
    sys.path_importer_cache.pop(module_dir, None)
    modules = list_all_modules(module_dir)
    for name in modules:
        module_path = "{}.{}".format(module.__name__, name)
        import_module(module_path)
        logger.info(f"{module_path} has been loaded")
