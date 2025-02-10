from pydantic import BaseModel, Field
from bk_operator_framework.generator.schemas import AdditionalPrinterColumn

# {{ plural }} is the plural form of {{ kind }}.
# Edit {{ singular }}_schemas.py and project_desc.yaml to update it.
{{ kind | upper }}_PLURAL = "{{ plural }}"


class {{ kind }}Spec(BaseModel):
    """
    {{ kind }}Spec defines the desired state of {{ kind }}.
    """
    foo: str = Field(description="Foo is an example field of {{ kind }}. Edit {{ singular }}_schemas.py to remove/update")


class {{ kind }}Status(BaseModel):
    """
    {{ kind }}Status defines the observed state of  {{ kind }}.
    """
    phase: str = Field(description="Phase is an example field of {{ kind }}. Edit {{ singular }}_schemas.py to remove/update")


class {{ kind }}(BaseModel):
    """
    {{ kind }} is the Schema for the {{ plural }} API.
    """
    spec: {{ kind }}Spec
    status: {{ kind }}Status


# Specifies additional columns returned in Table output.
# See https://kubernetes.io/docs/reference/using-api/api-concepts/#receiving-resources-as-tables for details.
# If no columns are specified, a single column displaying the age of the custom resource is used.
ADDITIONAL_PRINTER_COLUMN_LIST: list[AdditionalPrinterColumn] = []