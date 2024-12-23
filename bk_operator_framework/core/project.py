import os
import sys

import yaml

from bk_operator_framework.cli_actions import echo
from bk_operator_framework.core import template


class ProjectDesc:

    def __init__(self):
        self.domain = ""
        self.project_name = ""

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

        kwargs = {
            "target_relative_path": os.path.relpath(self.file_path, self.work_dir),
            "template_relative_path": os.path.join("init", "project_desc.yaml"),
            "render_vars": {
                "project_name": os.path.basename(self.work_dir),
                "domain": domain,
            },
        }
        template.create_file(**kwargs)

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


project_desc = ProjectDesc()
