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

import click


class CliText:
    INFO = click.style("INFO", fg="blue")
    FATA = click.style("FATA", fg="red")
    WARN = click.style("WARN", fg="yellow")


def info(message):
    click.echo(f"{CliText.INFO} {message}")


def warn(message):
    click.echo(f"{CliText.WARN} {message}")


def fata(message):
    click.echo(f"{CliText.FATA} {message}")
