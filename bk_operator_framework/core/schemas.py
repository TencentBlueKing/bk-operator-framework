from typing import Optional

from pydantic import BaseModel, Field


class GroupVersionSchema(BaseModel):
    group: str = Field(description="Resource Group")
    version: str = Field(description="Resource Version")

    def __str__(self):
        return f"GroupVersion -> {self.group}/{self.version}"


class ProjectResourceSchema(BaseModel):
    class Api(BaseModel):
        crdVersion: str = Field(description="K8s CustomResourceDefinition Version", default="v1")
        namespaced: bool = Field(description="Resource is namespaced (default true)", default=True)

    api: Optional[Api] = Field(description="Create Api Resource", default=None)
    controller: bool = Field(description="Create Controller")
    domain: str = Field(description="Resource Domain")
    group: str = Field(description="Resource Group")
    kind: str = Field(description="Resource Kind")
    plural: str = Field(description="Resource Plural")
    version: str = Field(description="Resource Version")
