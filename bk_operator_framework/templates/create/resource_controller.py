import kopf
from bk_operator_framework.core.schemas import RBACRule

from api.{{group}}.{{version}}.group_version import GROUP_VERSION
from api.{{group}}.{{version}}.{{singular}}_schemas import (
    {{ kind | upper }}_PLURAL,
    {{ kind }}Spec,
    {{ kind }}Status,
)

RBAC_RULE_LIST: list[RBACRule] = [
    RBACRule(apiGroups=[GROUP_VERSION.group], resources=[{{ kind | upper }}_PLURAL], verbs=["get", "list", "watch", "create", "update", "patch", "delete"]),
    RBACRule(apiGroups=[GROUP_VERSION.group], resources=[f"{{ '{' + kind | upper }}_PLURAL}/finalizers"], verbs=["update"]),
    RBACRule(apiGroups=[GROUP_VERSION.group], resources=[f"{{ '{' + kind | upper }}_PLURAL}/status"], verbs=["get", "update", "patch"])
]


@kopf.on.event(group=GROUP_VERSION.group, version=GROUP_VERSION.version, plural={{ kind | upper }}_PLURAL)
async def reconcile(spec, status, type, patch, logger, **kwargs):
    """
    Reconcile is part of the main kubernetes reconciliation loop which aims to
    move the current state of the cluster closer to the desired state.
    TODO(user): Modify the Reconcile function to compare the state specified by
    the {{ kind }} object against the actual cluster state, and then
    perform operations to make the cluster state reflect the state specified by the user.
    More information can be found here:
    https://kopf.readthedocs.io/en/stable/handlers/#event-watching-handlers
    """
    logger.info(f"Received {type} event, spec -> {spec}, status -> {status}.")

    spec_obj = {{ kind }}Spec(**spec)
    status_obj = {{ kind }}Status(**status) if status else None
    # TODO(user): your logic here

    # set the observed state of {{ kind }} object
    patch.setdefault("status", {}).update({{ kind }}Status(phase="Succeeded").model_dump())