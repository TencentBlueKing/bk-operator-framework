import kopf

from bk_operator_framework.core.schemas import GroupVersion

GROUP_VERSION = GroupVersion(group="{{ (group + '.' + domain).rstrip('.') }}", version="{{ version }}")
{{ kind | upper }}_PLURAL = "{{ plural }}"
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