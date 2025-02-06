import json
import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from bk_operator_framework.generator.cli_actions import echo
from bk_operator_framework.generator.schemas import ProjectResource

TEMPLATE_ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
WORK_DIR = os.getcwd()


def init_project_dir() -> None:
    """
    Init Project Dir
    :return:
    """
    init_template_dir = os.path.join(TEMPLATE_ROOT_DIR, "init")
    for root, dirs, files in os.walk(init_template_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(WORK_DIR, os.path.relpath(src_file, init_template_dir))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)


def render_file_with_vars(
    template_relative_path: str, target_relative_path: str, render_vars: dict[str:any] = None, default_env: bool = True
) -> None:
    """
    Render File With jinja2
    :param template_relative_path:
    :param target_relative_path:
    :param render_vars:
    :param default_env:
    :return:
    """
    if default_env:
        env = Environment(loader=FileSystemLoader(TEMPLATE_ROOT_DIR))
    else:
        env = Environment(
            loader=FileSystemLoader(TEMPLATE_ROOT_DIR),
            variable_start_string="<<",
            variable_end_string=">>",
            block_start_string="<%",
            block_end_string="%>",
            comment_start_string="<#",
            comment_end_string="#>",
        )

    env.filters["toJson"] = lambda x: json.dumps(x)
    template = env.get_template(template_relative_path)
    rendered_content = template.render(**render_vars)
    target_file = os.path.join(WORK_DIR, target_relative_path)
    with open(target_file, "w", encoding="utf-8") as file:
        file.write(rendered_content)


def render_file_with_keywords(template_relative_path: str, target_relative_path: str, keywords: dict[str:str]) -> None:
    """
    Render file by replacing keywords
    :param template_relative_path:
    :param target_relative_path:
    :param keywords:
    :return:
    """
    template_file_path = os.path.join(TEMPLATE_ROOT_DIR, template_relative_path)
    with open(template_file_path, encoding="utf-8") as file:
        rendered_content = file.read()
    for k, v in keywords.items():
        rendered_content = rendered_content.replace(k, v)
    target_file = os.path.join(WORK_DIR, target_relative_path)
    with open(target_file, "w", encoding="utf-8") as file:
        file.write(rendered_content)


def create_resource_api(group: str, version: str, kind: str, singular: str, plural: str, domain: str) -> None:
    """
    create resource api
    :param group:
    :param version:
    :param kind:
    :param singular:
    :param plural:
    :param domain:
    :return:
    """
    echo.info(f"api/{group}/{version}/group_version.py")
    echo.info(f"api/{group}/{version}/{singular}_schemas.py")

    resource_dir = os.path.join(WORK_DIR, "api", group, version)
    os.makedirs(resource_dir, exist_ok=True)

    group_init_path = os.path.join(WORK_DIR, "api", group, "__init__.py")
    open(group_init_path, "a").close()

    version_init_path = os.path.join(resource_dir, "__init__.py")
    open(version_init_path, "a").close()

    group_version_file_path = os.path.join(resource_dir, "group_version.py")
    if not os.path.exists(group_version_file_path):
        group_version_kwargs = {
            "target_relative_path": os.path.relpath(group_version_file_path, WORK_DIR),
            "template_relative_path": os.path.join("create", "group_version.py"),
            "render_vars": {"group": f"{group}.{domain}", "version": version},
        }
        render_file_with_vars(**group_version_kwargs)

    resource_schemas_path = os.path.join(resource_dir, f"{singular}_schemas.py")
    if os.path.exists(resource_schemas_path):
        echo.fata(f"failed to create api/{group}/{version}/{singular}_schemas.py: file already exists")
        sys.exit(1)

    resource_schemas_kwargs = {
        "target_relative_path": os.path.relpath(resource_schemas_path, WORK_DIR),
        "template_relative_path": os.path.join("create", "resource_schemas.py"),
        "render_vars": {"kind": kind, "plural": plural, "singular": singular},
    }
    render_file_with_vars(**resource_schemas_kwargs)


def create_resource_controller(
    group: str,
    version: str,
    kind: str,
    singular: str,
    plural: str,
    domain: str,
    external_api_domain: str,
    api: ProjectResource.Api,
):
    """
    create resource controller
    :param group:
    :param version:
    :param kind:
    :param singular:
    :param plural:
    :param domain:
    :param external_api_domain:
    :param api:
    :return:
    """
    echo.info(f"internal/controller/{singular}_controller.py")

    controller_dir = os.path.join(WORK_DIR, "internal", "controller")
    os.makedirs(controller_dir, exist_ok=True)

    controller_init_path = os.path.join(controller_dir, "__init__.py")
    open(controller_init_path, "a").close()

    resource_controller_path = os.path.join(controller_dir, f"{singular}_controller.py")
    if os.path.exists(resource_controller_path):
        echo.fata(f"failed to create internal/controller/{singular}_controller.py: file already exists")
        sys.exit(1)

    if external_api_domain is not None or not api:
        template_relative_path = os.path.join("create", "external_resource_controller.py")
    else:
        template_relative_path = os.path.join("create", "resource_controller.py")
    resource_controller_kwargs = {
        "target_relative_path": os.path.relpath(resource_controller_path, WORK_DIR),
        "template_relative_path": template_relative_path,
        "render_vars": {
            "kind": kind,
            "plural": plural,
            "singular": singular,
            "group": group,
            "domain": domain,
            "version": version,
        },
    }
    render_file_with_vars(**resource_controller_kwargs)

    return controller_dir


def create_resource_webhook(
    group: str,
    version: str,
    kind: str,
    singular: str,
    plural: str,
    domain: str,
    defaulting: bool,
    validation: bool,
    external_api_domain: str,
    api: ProjectResource.Api,
):
    """

    :param group:
    :param version:
    :param kind:
    :param singular:
    :param plural:
    :param domain:
    :param defaulting:
    :param validation:
    :param external_api_domain:
    :param api:
    :return:
    """
    echo.info(f"internal/webhook/{singular}_webhook.py")

    webhook_dir = os.path.join(WORK_DIR, "internal", "webhook")
    os.makedirs(webhook_dir, exist_ok=True)

    controller_init_path = os.path.join(webhook_dir, "__init__.py")
    open(controller_init_path, "a").close()

    resource_webhook_path = os.path.join(webhook_dir, f"{singular}_webhook.py")
    if os.path.exists(resource_webhook_path):
        echo.fata(f"failed to create internal/webhook/{singular}_webhook.py: file already exists")
        sys.exit(1)

    if external_api_domain is not None or not api:
        template_relative_path = os.path.join("create", "external_resource_webhook.py")
    else:
        template_relative_path = os.path.join("create", "resource_webhook.py")
    resource_webhook_kwargs = {
        "target_relative_path": os.path.relpath(resource_webhook_path, WORK_DIR),
        "template_relative_path": template_relative_path,
        "render_vars": {
            "kind": kind,
            "plural": plural,
            "singular": singular,
            "group": group,
            "version": version,
            "domain": domain,
            "defaulting": defaulting,
            "validation": validation,
        },
    }
    render_file_with_vars(**resource_webhook_kwargs)

    return webhook_dir


def create_or_update_chart_basic_file(project_name: str, chart_version: str, chart_app_version: str) -> str:
    """

    :param project_name:
    :param chart_version:
    :param chart_app_version:
    :return:
    """
    chart_dir = os.path.join(WORK_DIR, "chart")
    os.makedirs(chart_dir, exist_ok=True)

    helm_ignore_path = os.path.join(WORK_DIR, "chart", ".helmignore")
    if not os.path.exists(helm_ignore_path):
        echo.info("chart/.helmignore")
        helm_ignore_path_kwargs = {
            "target_relative_path": os.path.relpath(helm_ignore_path, WORK_DIR),
            "template_relative_path": os.path.join("chart", ".helmignore"),
            "render_vars": {},
        }
        render_file_with_vars(**helm_ignore_path_kwargs)

    chart_yaml_path = os.path.join(WORK_DIR, "chart", "Chart.yaml")
    echo.info("chart/Chart.yaml")
    if not os.path.exists(chart_yaml_path):
        chart_yaml_kwargs = {
            "target_relative_path": os.path.relpath(chart_yaml_path, WORK_DIR),
            "template_relative_path": os.path.join("chart", "Chart.yaml"),
            "render_vars": {"project_name": project_name, "version": chart_version, "appVersion": chart_app_version},
        }
        render_file_with_vars(**chart_yaml_kwargs)
    else:
        yaml = YAML()

        with open(chart_yaml_path) as file:
            data = yaml.load(file)

        data["version"] = chart_version
        data["appVersion"] = DoubleQuotedScalarString(chart_app_version)

        with open(chart_yaml_path, "w") as file:
            yaml.dump(data, file)

    return chart_dir


def create_or_update_chart_crds(resource_versions: list[ProjectResource]) -> None:
    """
    :param resource_versions:
    :return:
    """
    crds_dir = os.path.join(WORK_DIR, "chart", "crds")
    os.makedirs(crds_dir, exist_ok=True)

    _resource = resource_versions[-1]["resource"]

    meta = {
        "crdVersion": _resource.api.crdVersion,
        "name": f"{_resource.plural}.{_resource.group}.{_resource.domain}",
        "group": f"{_resource.group}.{_resource.domain}",
        "namespaced": _resource.api.namespaced,
        "plural": _resource.plural,
        "singular": _resource.singular,
        "kind": _resource.kind,
    }
    crd_yaml_path = os.path.join(crds_dir, f'{meta["name"]}.yaml')
    target_relative_path = os.path.relpath(crd_yaml_path, WORK_DIR)
    echo.info(target_relative_path)
    chart_yaml_kwargs = {
        "target_relative_path": os.path.relpath(crd_yaml_path, WORK_DIR),
        "template_relative_path": os.path.join("chart", "crds", "crd.yaml"),
        "render_vars": {"meta": meta, "resource_versions": resource_versions},
    }
    render_file_with_vars(**chart_yaml_kwargs)

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(crd_yaml_path) as file:
        data = yaml.load(file)
    for index, version in enumerate(data["spec"]["versions"]):
        version["schema"]["openAPIV3Schema"] = resource_versions[index]["openapi_v3_schema"]
    with open(crd_yaml_path, "w") as file:
        yaml.dump(data, file)


def create_or_update_chart_templates(
    project_name: str,
    cluster_role_rule_list: list,
    validating_webhooks: list,
    mutating_webhooks: list,
    exist_controller: bool,
    exist_webhook: bool,
):
    """
    :param project_name:
    :param cluster_role_rule_list:
    :param validating_webhooks:
    :param mutating_webhooks:
    :param exist_controller:
    :param exist_webhook:
    :return:
    """
    chart_templates_dir = os.path.join(WORK_DIR, "chart", "templates")
    os.makedirs(chart_templates_dir, exist_ok=True)

    raw_chart_templates_dir = os.path.join(TEMPLATE_ROOT_DIR, "chart", "templates")

    for template_relative_path in os.listdir(raw_chart_templates_dir):
        if not exist_controller and template_relative_path == "controller-deployment.yaml":
            continue
        if not exist_webhook and template_relative_path in {
            "admissionwebhook.yaml",
            "webhook-deployment.yaml",
            "webhook-service.yaml",
        }:
            continue

        target_file_path = os.path.join(chart_templates_dir, template_relative_path)
        target_relative_path = os.path.relpath(target_file_path, WORK_DIR)
        echo.info(target_relative_path)

        if template_relative_path in {"clusterrole.yaml", "admissionwebhook.yaml"}:
            create_kwargs = {
                "target_relative_path": target_relative_path,
                "template_relative_path": os.path.join("chart", "templates", template_relative_path),
                "render_vars": {
                    "project_name": project_name,
                    "cluster_role_rule_list": cluster_role_rule_list,
                    "validating_webhooks": validating_webhooks,
                    "mutating_webhooks": mutating_webhooks,
                },
                "default_env": False,
            }
            render_file_with_vars(**create_kwargs)
            continue
        else:
            create_kwargs = {
                "target_relative_path": target_relative_path,
                "template_relative_path": os.path.join("chart", "templates", template_relative_path),
                "keywords": {"bof_tmp_project": project_name},
            }
            render_file_with_keywords(**create_kwargs)


def create_chart_values(project_name: str, exist_controller: bool, exist_webhook: bool) -> None:
    """
    :param project_name:
    :param exist_webhook:
    :param exist_controller:
    :return:
    """
    chart_values_path = os.path.join(WORK_DIR, "chart", "values.yaml")
    if not os.path.exists(chart_values_path):
        echo.info("chart/values.yaml")
        chart_yaml_kwargs = {
            "target_relative_path": os.path.relpath(chart_values_path, WORK_DIR),
            "template_relative_path": os.path.join("chart", "values.yaml"),
            "render_vars": {
                "project_name": project_name,
                "exist_controller": exist_controller,
                "exist_webhook": exist_webhook,
            },
        }
        render_file_with_vars(**chart_yaml_kwargs)
