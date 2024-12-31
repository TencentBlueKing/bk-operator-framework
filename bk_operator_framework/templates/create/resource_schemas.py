from pydantic import BaseModel, Field
from bk_operator_framework.core.schemas import AdditionalPrinterColumnSchema

# {{ plural }} is the plural form of {{ kind }}.
# Edit {{ singular }}_schemas.py and project_desc.yaml to update it.
{{ kind }}Plural = "{{ plural }}"


class {{ kind }}Spec(BaseModel):
    """
    {{ kind }}Spec defines the desired state of {{ kind }}.
    """
    foo: str = Field(description="Foo is an example field of {{ kind }}. Edit {{ singular }}_schemas.py to remove/update")


class {{ kind }}Status(BaseModel):
    """
    {{ kind }}Status defines the desired state of {{ kind }}.
    """
    pass


class {{ kind }}(BaseModel):
    """
    {{ kind }} is the Schema for the {{ plural }} API.
    """
    spec: {{ kind }}Spec
    status: {{ kind }}Status


# Specifies additional columns returned in Table output.
# See https://kubernetes.io/docs/reference/using-api/api-concepts/#receiving-resources-as-tables for details.
# If no columns are specified, a single column displaying the age of the custom resource is used.
{{ kind }}AdditionalPrinterColumnList: list[AdditionalPrinterColumnSchema] = []