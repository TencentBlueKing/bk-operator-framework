import os
import sys

import yaml

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template
from bk_operator_framework.core.schemas import ProjectChart, ProjectResource


class ProjectDesc:

    def __init__(self):
        self.domain = None
        self.project_name = None
        self.resources = []
        self.chart = None

        self.work_dir = os.getcwd()
        self.file_path = os.path.join(self.work_dir, "project_desc.yaml")

    @property
    def is_initialized(self):
        """
        Is the project initialized?
        :return: True/False
        """
        return os.path.exists(self.file_path)

    def init_basc_info(self, domain):
        """
        init project desc
        :param domain:
        :return:
        """
        self.project_name = os.path.basename(self.work_dir).lower().replace("_", "-")
        self.domain = domain
        self.render()

    def reload(self):
        """
        reload with the project_desc.yaml
        :return:
        """
        if not self.is_initialized:
            echo.fata("project_desc.yaml does not exist.")
            sys.exit(1)

        with open(self.file_path) as file:
            data = yaml.safe_load(file)

        self.domain = data["domain"]
        self.project_name = data["project_name"]

        self.resources = [ProjectResource(**r) for r in data.get("resources", [])]
        self.chart = data.get("chart") and ProjectChart(**data.get("chart"))

    def render(self):
        """
        Render Project Info to project_desc.yaml
        :return:
        """
        kwargs = {
            "target_relative_path": os.path.relpath(self.file_path, self.work_dir),
            "template_relative_path": os.path.join("init", "project_desc.yaml"),
            "render_vars": {"project_desc": self},
        }

        template.create_file(**kwargs)
        echo.info("project_desc.yaml")

    def create_or_update_resource(
        self,
        group: str,
        version: str,
        kind: str,
        plural: str = None,
        resource: bool = None,
        controller: bool = None,
        namespaced: bool = None,
        webhooks: dict = None,
        external_api_domain: str = None,
    ) -> ProjectResource:
        """
        Create Or update resources
        """
        self.reload()
        singular = kind.lower()
        if plural is None:
            plural = f"{singular}s"
        domain = external_api_domain if external_api_domain is not None else self.domain
        desire_resource_key = f"{plural}.{group}.{domain}/{version}"

        live_resource = None
        for r in self.resources:
            _exist_resource_key = f"{r.plural}.{r.group}.{r.domain}/{r.version}"
            if desire_resource_key == _exist_resource_key:
                live_resource = r
                break

        if live_resource:
            if resource and not live_resource.api:
                live_resource.api = ProjectResource.Api(namespaced=namespaced)
            if controller and not live_resource.controller:
                live_resource.controller = True
            if webhooks is not None:
                live_resource.webhooks = ProjectResource.Webhook(**webhooks)

            return live_resource
        else:
            desire_resource_info = {
                "group": group,
                "version": version,
                "kind": kind,
                "singular": singular,
                "plural": plural,
                "domain": domain,
            }
            if resource:
                desire_resource_info.update({"api": {"namespaced": namespaced}})
            if controller is not None:
                desire_resource_info["controller"] = controller
            if webhooks is not None:
                desire_resource_info["webhooks"] = webhooks
            desire_resource = ProjectResource(**desire_resource_info)
            self.resources.append(desire_resource)

            return desire_resource

    def create_or_update_chart(self, part):
        if not self.chart:
            self.chart = ProjectChart()
            self.chart.bump_app_version()
        else:
            self.chart.bump_version(part)
            self.chart.bump_app_version()


project_desc = ProjectDesc()
