import kopf
from api.{{group}}.{{version}}.group_version import GroupVersion
from api.{{group}}.{{version}}.{{singular}}_schemas import (
    {{ kind }}Plural,
    {{ kind }}Spec,
    {{ kind }}Status,
)


@kopf.on.event(group=GroupVersion.group, version=GroupVersion.version, plural={{ kind }}Plural)
async def reconcile(spec, **kwargs):
    spec_obj = {{ kind }}Spec(**spec)
    print(f"Hello, {spec_obj.foo}")

    return {{ kind }}Status().model_dump()
