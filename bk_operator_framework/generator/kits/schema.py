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

import copy
import sys

from bk_operator_framework.generator.cli_actions import echo

CRD_SCHEMA_NOT_ALLOW_SET_FIELD_LIST = [
    "definitions",
    "dependencies",
    "deprecated",
    "discriminator",
    "id",
    "patternProperties",
    "readOnly",
    "writeOnly",
    "xml",
    "$ref",
]


def schema_validate(properties):
    title = properties.get("title", [])
    if "uniqueItems" in properties and properties["uniqueItems"] is True:
        echo.fata(f"The field[{title}] uniqueItems cannot be set to true.")
        sys.exit(1)

    if "additionalProperties" in properties and properties["additionalProperties"] is False:
        echo.fata(f"The field[{title}] additionalProperties cannot be set to false.")
        sys.exit(1)

    if "additionalProperties" in properties and "properties" in properties:
        echo.fata(f"The field[{title}] additionalProperties is mutually exclusive with properties.")
        sys.exit(1)


def get_openapi_v3_schema(schema_model):
    schema = schema_model.model_json_schema()

    def _trim_properties(_properties):
        if "$ref" in _properties:
            _child_cls_name = _properties["$ref"].split("/")[-1]
            _properties.update(schema["$defs"][_child_cls_name])
            for _k, _v in _properties["properties"].items():
                _properties["properties"][_k] = _trim_properties(_v)

        if "items" in _properties and "$ref" in _properties["items"]:
            _child_cls_name = _properties["items"]["$ref"].split("/")[-1]
            _properties["items"].update(schema["$defs"][_child_cls_name])
            for _k, _v in _properties["items"]["properties"].items():
                _properties["items"]["properties"][_k] = _trim_properties(_v)

        __properties = copy.deepcopy(_properties)
        schema_validate(_properties)
        for _k, _v in _properties.items():
            if _k in CRD_SCHEMA_NOT_ALLOW_SET_FIELD_LIST:
                __properties.pop(_k)

        schema_validate(_properties.get("items", {}))
        for _k, _v in _properties.get("items", {}).items():
            if _k in CRD_SCHEMA_NOT_ALLOW_SET_FIELD_LIST:
                __properties.pop(_k)

        return __properties

    properties = {}
    for k, v in schema["properties"].items():
        properties[k] = _trim_properties(v)

    return {"type": schema["type"], "properties": properties}
