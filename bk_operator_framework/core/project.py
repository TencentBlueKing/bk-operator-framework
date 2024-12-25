import os
import sys

import yaml

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template
from bk_operator_framework.core.schemas import ProjectChartSchema, ProjectResourceSchema


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
        self.project_name = os.path.basename(self.work_dir)
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

        self.domain = data.get("domain", "")
        self.project_name = data.get("project_name", "")

        self.resources = [ProjectResourceSchema(**r) for r in data.get("resources", [])]
        self.chart = data.get("chart") and ProjectChartSchema(**data.get("chart"))

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

    def create_or_update_resources(self, group, version, kind, plural, singular, resource, controller, namespaced):
        """
        Create Or update resources
        :param group:
        :param version:
        :param kind:
        :param plural:
        :param singular:
        :param resource:
        :param controller:
        :param namespaced:
        :return:
        """
        resource_info = {
            "group": group,
            "version": version,
            "kind": kind,
            "singular": singular,
            "plural": plural,
            "controller": controller,
            "domain": self.domain,
        }
        if resource:
            resource_info.update({"api": {"namespaced": namespaced}})
        resource = ProjectResourceSchema(**resource_info)
        resource_exist = False
        for index, old_resource in enumerate(self.resources):
            if (resource.group, resource.domain, resource.version, resource.kind, resource.plural) == (
                old_resource.group,
                old_resource.domain,
                old_resource.version,
                old_resource.kind,
                old_resource.plural,
            ):
                if old_resource.api:
                    resource.api = old_resource.api

                if old_resource.controller:
                    resource.controller = old_resource.controller

                self.resources[index] = resource
                resource_exist = True
                break

        if not resource_exist:
            self.resources.append(resource)

    def create_or_update_chart(self, part):
        if not self.chart:
            self.chart = ProjectChartSchema()
            self.chart.bump_app_version()
        else:
            self.chart.bump_version(part)
            self.chart.bump_app_version()


project_desc = ProjectDesc()
