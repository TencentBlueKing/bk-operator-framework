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

import click

from bk_operator_framework.generator import cli_actions

sys.path.append(os.getcwd())


@click.group(name="bof", epilog='Use "bof [command] --help" for more information about a command.')
def bof() -> None:
    """CLI tool for building Kubernetes extensions and tools."""
    pass


@bof.command()
def version() -> None:
    """Print the bof version."""
    cli_actions.version.main()


@bof.command()
@click.option("--domain", type=str, default="my.domain", help="Resource Group")
def init(domain: str) -> None:
    """Initialize a new bof project."""
    cli_actions.init.main(domain)


@bof.group(
    help="Scaffold a Kubernetes API or webhook.",
    epilog='Use "bof create [command] --help" for more information about a command.',
)
def create() -> None:
    """Scaffold a Kubernetes API or webhook."""
    pass


@create.command(help="Scaffold a Kubernetes API")
@click.option("--group", type=str, required=True, help="Resource Group")
@click.option("--version", type=str, required=True, help="Resource Version")
@click.option("--kind", type=str, required=True, help="Resource Kind")
@click.option("--plural", type=str, help="resource irregular plural form")
@click.option("--namespaced", type=bool, default=True, help="Resource is namespaced (default true)")
@click.option(
    "--resource",
    type=bool,
    prompt=f"{cli_actions.CliText.INFO} Create Resource [y/N]",
    help="if set, generate the resource without prompting the user",
)
@click.option(
    "--controller",
    type=bool,
    prompt=f"{cli_actions.CliText.INFO} Create Controller [y/N]",
    help="if set, generate the controller without prompting the user",
)
@click.option(
    "--external-api-domain",
    type=str,
    help="Specify the domain name for the external API. This domain is used to generate accurate RBAC markers and permissions for the external resources",
)
def api(
    group: str,
    version: str,
    kind: str,
    plural: str,
    namespaced: str,
    controller: bool,
    resource: bool,
    external_api_domain: str,
) -> None:
    cli_actions.create_api.main(group, version, kind, plural, namespaced, controller, resource, external_api_domain)


@create.command(help="Scaffold a webhook for an API resource")
@click.option("--group", type=str, required=True, help="Resource Group")
@click.option("--version", type=str, required=True, help="Resource Version")
@click.option("--kind", type=str, required=True, help="Resource Kind")
@click.option("--plural", type=str, help="resource irregular plural form")
@click.option("--defaulting", type=bool, is_flag=True, help="if set, scaffold the defaulting webhook")
@click.option("--validation", type=bool, is_flag=True, help="if set, scaffold the validating webhook")
@click.option(
    "--external-api-domain",
    type=str,
    help="Specify the domain name for the external API. This domain is used to generate accurate RBAC markers and permissions for the external resources",
)
def webhook(
    group: str, version: str, kind: str, plural: str, defaulting: bool, validation: bool, external_api_domain: str
):
    cli_actions.create_webhook.main(group, version, kind, plural, defaulting, validation, external_api_domain)


@bof.command()
@click.option(
    "--part",
    type=click.Choice(["major", "minor", "patch"]),
    help="Helm Chart Semantic Versioning Part",
    default="patch",
)
def chart(part):
    """Generate helm chart for the project."""
    cli_actions.chart.main(part)


if __name__ == "__main__":
    bof(prog_name="bof")
