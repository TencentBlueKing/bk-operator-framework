import kopf
from bk_operator_framework.core.schemas import ClusterRoleRuleSchema

from api.{{group}}.{{version}}.group_version import GroupVersion
from api.{{group}}.{{version}}.{{singular}}_schemas import (
    {{ kind }}Plural,
    {{ kind }}Spec,
    {{ kind }}Status,
)

ServiceAccountClusterRoleRuleList: list[ClusterRoleRuleSchema] = [
    ClusterRoleRuleSchema(apiGroups=[GroupVersion.group], resources=[{{ kind }}Plural], verbs=["*"]),
    ClusterRoleRuleSchema(apiGroups=[GroupVersion.group], resources=[f"{{ '{' + kind }}Plural}/finalizers"], verbs=["update"]),
    ClusterRoleRuleSchema(apiGroups=[GroupVersion.group], resources=[f"{{ '{' + kind }}Plural}/status"], verbs=["get", "update", "patch"])
]


@kopf.on.event(group=GroupVersion.group, version=GroupVersion.version, plural={{ kind }}Plural)
async def reconcile(spec, status, type, patch, logger, **kwargs):
    """
    Reconcile is part of the main kubernetes reconciliation loop which aims to
    move the current state of the cluster closer to the desired state.
    TODO(user): Modify the Reconcile function to compare the state specified by
    the {{ kind }} object against the actual cluster state, and then
    perform operations to make the cluster state reflect the state specified by the user.
    """
    logger.info(f"Received {type} event, spec -> {spec}, status -> {status}.")

    spec_obj = {{ kind }}Spec(**spec)
    status_obj = {{ kind }}Status(**status) if status else None
    # TODO(user): your logic here

    # set the observed state of {{ kind }} object
    patch.setdefault("status", {}).update({{ kind }}Status(phase="Succeeded").model_dump())