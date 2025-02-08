import kopf
from bk_operator_framework.generator.schemas import GroupVersion

GROUP_VERSION = GroupVersion(group="{{ (group + '.' + domain).rstrip('.') }}", version="{{ version }}")
{{ kind | upper }}_PLURAL = "{{ plural }}"
{%- if defaulting %}


@kopf.on.mutate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, id="set-{{ singular }}-default")
async def set_{{ singular }}_default(spec, patch, logger, **kwargs):
    """
    Setting default values on the custom resource of the Kind {{ kind }} when those are created or updated.
    More information can be found here:
    https://kopf.readthedocs.io/en/stable/admission/#mutation-handlers
    """
    logger.info(f"Defaulting for {{ kind }}, spec is {spec}")

    # TODO(user): fill in your defaulting logic.
{%- endif %}
{%- if validation %}


@kopf.on.validate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, operations=["CREATE"], id="validate-{{ singular }}-create")
async def validate_{{ singular }}_create(spec, logger, **kwargs):
    """
    Validating the {{ kind }} resource when it is created.
    More information can be found here:
    https://kopf.readthedocs.io/en/stable/admission/#validation-handlers
    """
    logger.info(f"Validation for {{ kind }} upon creation, spec is {spec}.")

    # TODO(user): fill in your validation logic upon object creation.


@kopf.on.validate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, operations=["UPDATE"], id="validate-{{ singular }}-update")
async def validate_{{ singular }}_update(spec, logger, **kwargs):
    """
    Validating the {{ kind }} resource when it is updated.
    More information can be found here:
    https://kopf.readthedocs.io/en/stable/admission/#validation-handlers
    """
    logger.info(f"Validation for {{ kind }} upon update, spec is {spec}.")

    # TODO(user): fill in your validation logic upon object update.


@kopf.on.validate(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL, operations=["DELETE"], id="validate-{{ singular }}-delete")
async def validate_{{ singular }}_delete(spec, logger, **kwargs):
    """
    Validating the {{ kind }} resource when it is deleted.
    More information can be found here:
    https://kopf.readthedocs.io/en/stable/admission/#validation-handlers
    """
    logger.info(f"Validation for {{ kind }} upon deletion, spec is {spec}")

    # TODO(user): fill in your validation logic upon object deletion.
{% endif %}