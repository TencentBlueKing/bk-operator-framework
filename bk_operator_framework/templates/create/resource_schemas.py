from pydantic import BaseModel, Field

# {{ plural }} is the plural form of {{ kind }}. Edit {{ singular }}_schemas.py and project_desc.yaml to update it.
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

