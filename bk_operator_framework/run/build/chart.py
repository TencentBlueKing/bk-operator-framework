import copy
import re
from datetime import datetime

import yaml

chart_template_dict = {
    "apiVersion": "v2",
    "name": "workload-restart",
    "description": "An operator that restarts sequentially by adjusting the number of workload replicas",
    "type": "application",
    "version": "1.0.0-build.202310010912",
    "appVersion": "1.0.0",
}


def build_chart_yaml(operator_cls, chart_yaml_path, chart_dict, target_string):
    chart_dict = chart_dict or copy.deepcopy(chart_template_dict)

    match = re.match(r"(\d+)\.(\d+)\.(\d+)", chart_dict["version"])
    major, minor, patch = map(int, match.groups())
    current_date = datetime.now().strftime("%Y%m%d%H%M")
    chart_dict["version"] = f"{major}.{minor}.{patch + 1}-build.{current_date}"

    chart_dict["name"] = operator_cls.Meta.singular
    chart_dict["appVersion"] = f"{target_string}.build.{current_date}"
    chart_dict["description"] = operator_cls.Meta.description
    with open(chart_yaml_path, "w") as file:
        yaml.dump(chart_dict, file)
