import copy
import datetime
from typing import Optional

import semver
from pydantic import BaseModel, Field

_JSON_SCHEMA_KEY_LIST = ["type", "default", "description", "items", "properties"]


class GroupVersionSchema(BaseModel):
    group: str = Field(description="Resource Group")
    version: str = Field(description="Resource Version")

    def __str__(self):
        return f"GroupVersion -> {self.group}/{self.version}"


class ProjectResourceSchema(BaseModel):
    class Api(BaseModel):
        crdVersion: str = Field(description="K8s CustomResourceDefinition Version", default="v1")
        namespaced: bool = Field(description="Resource is namespaced (default true)", default=True)
        storage: bool = Field(
            description="served is a flag enabling/disabling this version from being served via REST APIs", default=True
        )
        served: bool = Field(
            description="storage indicates this version should be used when persisting custom resources to storage. "
            "There must be exactly one version with storage=true.",
            default=True,
        )

    api: Optional[Api] = Field(description="Create Api Resource", default=None)
    controller: bool = Field(description="Create Controller")
    domain: str = Field(description="Resource Domain")
    group: str = Field(description="Resource Group")
    kind: str = Field(description="Resource Kind")
    plural: str = Field(description="Resource Plural")
    singular: str = Field(description="Resource Singular")
    version: str = Field(description="Resource Version")


class ProjectChartSchema(BaseModel):
    version: str = Field(description="Helm Chart Version", default="0.0.1")
    appVersion: str = Field(description="Helm Chart appVersion", default="1.16.0")

    def bump_app_version(self, app_version=None):
        self.appVersion = app_version if app_version else datetime.datetime.now().strftime("build.%Y-%m-%d_%H-%M")

    def bump_version(self, part="patch"):
        self.version = str(semver.VersionInfo.parse(self.version).next_version(part))


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
        for _k, _v in _properties.items():
            if _k not in _JSON_SCHEMA_KEY_LIST:
                __properties.pop(_k)

        for _k, _v in _properties.get("items", {}).items():
            if _k not in _JSON_SCHEMA_KEY_LIST:
                __properties["items"].pop(_k)

        return __properties

    properties = {}
    for k, v in schema["properties"].items():
        properties[k] = _trim_properties(v)

    return {"type": schema["type"], "properties": properties}
