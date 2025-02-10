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

from setuptools import find_packages, setup

setup(
    name="bk_operator_framework",
    version="1.0.0",
    packages=find_packages(include=["bk_operator_framework", "bk_operator_framework.*"]),
    include_package_data=True,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "bof=bk_operator_framework.cli:bof",
        ],
    },
    install_requires=[
        "click==8.1.7",
        "Jinja2===3.1.4",
        "pydantic==2.10.3",
        "PyYAML==6.0.2",
        "ruamel.yaml==0.18.6",
        "semver==3.0.2",
        "kopf==1.37.4",
        "kubernetes==31.0.0",
    ],
)
