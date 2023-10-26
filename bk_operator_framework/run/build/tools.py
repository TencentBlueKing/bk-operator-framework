import os
import shutil
import subprocess
from importlib import import_module

import yaml

from bk_operator_framework.hub.operator import OperatorHub
from bk_operator_framework.run.build.app import build_app_yaml
from bk_operator_framework.run.build.chart import build_chart_yaml
from bk_operator_framework.run.build.crd import build_crd_yaml
from bk_operator_framework.run.build.helm_ignore import build_helm_ignore
from bk_operator_framework.run.build.rbac import build_rbac_yaml
from bk_operator_framework.run.build.values import build_values_yaml
from bk_operator_framework.utils.module_load import discover_operators


def build(**build_kwargs):
    discover_operators(import_module("bk_operator.versions"))

    work_dir = os.getcwd()
    target_string = build_kwargs.get("target_string")
    if ":" not in target_string:
        target_string = "{}:latest".format(target_string)
    skip_image = build_kwargs.get("skip_image")
    push_image = build_kwargs.get("push_image")

    if not skip_image:
        command = "docker build -t {} {}".format(target_string, work_dir)
        subprocess.check_call(command, shell=True)

    if push_image:
        command = "docker push {}".format(target_string)
        subprocess.check_call(command, shell=True)

    helm_charts_base_dir = os.path.join(work_dir, "helm_charts")

    for version, operator_cls in OperatorHub.all_versions().items():
        version_helm_charts_dir = os.path.join(helm_charts_base_dir, version)
        chart_yaml_path = os.path.join(version_helm_charts_dir, "Chart.yaml")
        chart_dict = {}
        if os.path.exists(chart_yaml_path):
            with open(chart_yaml_path, "r") as file:
                chart_dict = yaml.safe_load(file)

        if os.path.exists(version_helm_charts_dir):
            shutil.rmtree(version_helm_charts_dir)

        os.makedirs(version_helm_charts_dir)

        build_chart_yaml(operator_cls, chart_yaml_path, chart_dict, target_string)
        build_helm_ignore(version_helm_charts_dir)
        build_app_yaml(operator_cls, version_helm_charts_dir)
        build_crd_yaml(operator_cls, version_helm_charts_dir)
        build_rbac_yaml(operator_cls, version_helm_charts_dir)
        build_values_yaml(operator_cls, version_helm_charts_dir, target_string)

        print("[{}]  has been generated successfully!!!".format(operator_cls))
