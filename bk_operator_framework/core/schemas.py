import datetime
from typing import Optional

import semver
from pydantic import BaseModel, Field


class GroupVersionSchema(BaseModel):
    group: str = Field(description="Resource Group")
    version: str = Field(description="Resource Version")

    def __str__(self):
        return f"GroupVersion -> {self.group}/{self.version}"


class AdditionalPrinterColumnSchema(BaseModel):
    name: str = Field(description="A human readable name for the column")
    type: str = Field(description="An OpenAPI type definition for this column")
    jsonPath: str = Field(
        description="A simple JSON path (i.e. with array notation) which is evaluated against each custom resource to produce the value for this column"
    )
    description: str = Field(description="A human readable description of this column", default=None)
    priority: int = Field(
        description="priority is an integer defining the relative importance of this column compared to others."
        "Lower numbers are considered higher priority. Columns that may be omitted in limited space scenarios should be given a priority greater than 0.",
        default=None,
    )
    format: str = Field(
        description="format is an optional OpenAPI type definition for this column."
        "The 'name' format is applied to the primary identifier column to assist in clients identifying column is the resource name",
        default=None,
    )


class ClusterRoleRuleSchema(BaseModel):
    apiGroups: list[str] = Field(
        description="APIGroups is the name of the APIGroup that contains the resources."
        "If multiple API groups are specified, any action requested against one of the enumerated resources in any API group will be allowed."
        " '' represents the core API group and ' * ' represents all API groups."
    )
    resources: list[str] = Field(
        description="Resources is a list of resources this rule applies to. '*' represents all resources."
    )
    verbs: list[str] = Field(
        description="Verbs is a list of Verbs that apply to ALL the ResourceKinds contained in this rule. '*' represents all verbs."
    )

    resourceNames: list[str] = Field(
        description="ResourceNames is an optional white list of names that the rule applies to. An empty set means that everything is allowed.",
        default=None,
    )
    nonResourceURLs: list[str] = Field(
        description="NonResourceURLs is a set of partial urls that a user should have access to. *s are allowed"
        "but only as the full, final step in the path Since non-resource URLs are not namespaced,"
        "this field is only applicable for ClusterRoles referenced from a ClusterRoleBinding."
        "Rules can either apply to API resources (such as 'pods' or 'secrets') or non-resource URL paths (such as '/api'), but not both.",
        default=None,
    )


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
