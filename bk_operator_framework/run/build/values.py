import copy
import os

import yaml

values_template_dict = {
    "replicaCount": 1,
    "appName": "workload-restart",
    "image": {"repository": "", "pullPolicy": "IfNotPresent", "tag": ""},
    "serviceAccount": {"create": True, "name": "workload-restart-service-account"},
    "env": {},
}


def build_values_yaml(operator_cls, version_helm_charts_dir, target_string):
    values_yaml_path = os.path.join(version_helm_charts_dir, "values.yaml")
    values_dict = copy.deepcopy(values_template_dict)
    values_dict["serviceAccount"] = operator_cls._get_rbac_schema()["service_account"]
    values_dict["appName"] = operator_cls.Meta.singular

    values_dict["image"]["repository"] = target_string.split(":")[0]
    values_dict["image"]["tag"] = target_string.split(":")[1]
    for env_key in operator_cls.CUSTOM_ENVIRONMENT_KEY:
        values_dict["env"].setdefault(env_key, "")
    with open(values_yaml_path, "w") as file:
        yaml.dump(values_dict, file)
