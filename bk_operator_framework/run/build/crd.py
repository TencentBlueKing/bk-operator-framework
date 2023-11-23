import copy
import os

import yaml

crd_template_dict = {
    "apiVersion": "apiextensions.k8s.io/v1",
    "kind": "CustomResourceDefinition",
    "metadata": {"name": ""},
    "spec": {
        "group": "",
        "names": {"plural": "", "singular": "", "kind": "", "listKind": ""},
        "scope": "",
        "versions": [],
    },
    "status": {"acceptedNames": {"kind": "", "plural": ""}, "conditions": [], "storedVersions": []},
}

crd_version_template_dict = {
    "name": "",
    "served": None,
    "storage": None,
    "schema": {
        "openAPIV3Schema": {
            "type": "object",
            "properties": {
                "spec": {"properties": {}, "type": "object"},
                "status": {"properties": {}, "type": "object"},
            },
        }
    },
    "additionalPrinterColumns": [],
}


def extract_print_columns(d, parent_dict_path, print_columns=None):
    if print_columns is None:
        print_columns = []

    keys_to_remove = []
    for key, value in d.items():
        if isinstance(value, dict):
            _parent_dict_path = "{}.{}".format(parent_dict_path, key)
            extract_print_columns(value, _parent_dict_path, print_columns)
        elif key.startswith("print_column"):
            keys_to_remove.append(key)
            if key == "print_column" and value:
                name = "".join([word.capitalize() for word in parent_dict_path.split(".")[-1].split("_")])
                _print = {
                    "name": d.get("print_column__name") or name,
                    "type": d.get("type"),
                    "jsonPath": parent_dict_path.replace(".properties", ""),
                }
                if d.get("print_column__priority"):
                    _print["priority"] = d.get("print_column__priority")

                if d.get("description"):
                    _print["description"] = d.get("description")

                print_columns.append(_print)

    for key in keys_to_remove:
        d.pop(key)

    return print_columns


def build_crd_yaml(operator_cls, version_helm_charts_dir):
    template_helm_charts_dir = os.path.join(version_helm_charts_dir, "templates", "crd")
    if not os.path.exists(template_helm_charts_dir):
        os.makedirs(template_helm_charts_dir)

    spec_schema = operator_cls._get_spec_schema()
    status_schema = operator_cls._get_status_schema()

    spec_schema_properties = spec_schema["properties"]
    status_schema_properties = status_schema["properties"]

    crd_instance_dict = copy.deepcopy(crd_template_dict)
    crd_instance_dict["metadata"]["name"] = operator_cls.Meta.name
    crd_instance_dict["spec"]["group"] = operator_cls.Meta.group
    crd_instance_dict["spec"]["names"]["plural"] = operator_cls.Meta.plural
    crd_instance_dict["spec"]["names"]["singular"] = operator_cls.Meta.singular
    crd_instance_dict["spec"]["names"]["kind"] = operator_cls.Meta.kind
    crd_instance_dict["spec"]["names"]["listKind"] = operator_cls.Meta.listKind
    if getattr(operator_cls.Meta, "shortNames", None):
        crd_instance_dict["spec"]["names"]["shortNames"] = operator_cls.Meta.shortNames
    crd_instance_dict["spec"]["scope"] = operator_cls.Meta.scope

    crd_version_instance_dict = copy.deepcopy(crd_version_template_dict)
    crd_version_instance_dict["name"] = operator_cls.Meta.version
    crd_version_instance_dict["served"] = operator_cls.Meta.served
    crd_version_instance_dict["storage"] = operator_cls.Meta.storage
    crd_version_instance_dict["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"] = spec_schema_properties
    crd_version_instance_dict["schema"]["openAPIV3Schema"]["properties"]["status"][
        "properties"
    ] = status_schema_properties
    crd_instance_dict["spec"]["versions"].append(crd_version_instance_dict)

    spec_print_columns = extract_print_columns(spec_schema, ".spec")
    status_print_columns = extract_print_columns(status_schema, ".status")
    crd_version_instance_dict["additionalPrinterColumns"] = spec_print_columns + status_print_columns

    crd_yaml_path = os.path.join(template_helm_charts_dir, "{}.yaml".format(operator_cls.Meta.name))
    with open(crd_yaml_path, "w") as file:
        yaml.dump(crd_instance_dict, file)
