import kopf

from api.{{group}}.{{version}}.group_version import GROUP_VERSION
from api.{{group}}.{{version}}.{{singular}}_schemas import (
    {{ kind | upper }}_PLURAL,
    {{ kind }}Spec,
    {{ kind }}Status,
)
{%- if defaulting %}


@kopf.on.mutate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL)
async def default(spec, patch, logger, **kwargs):
    pass
{%- endif %}
{%- if validation %}


@kopf.on.validate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, operations=["CREATE"])
async def validate_create(spec, warnings, **kwargs):
    pass


@kopf.on.validate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, operations=["UPDATE"])
async def validate_update(spec, warnings, **kwargs):
    pass


@kopf.on.validate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, operations=["DELETE"])
async def validate_delete(spec, warnings, **kwargs):
    pass
{% endif %}