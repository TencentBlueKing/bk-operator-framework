import kopf

from bk_operator_framework.core.schemas import ClusterRoleRuleSchema
from bk_operator_framework.core.schemas import GroupVersionSchema

GroupVersion = GroupVersionSchema(group="{{ group }}", version="{{ version }}")
{{ kind }}Plural = "{{ plural }}"

ServiceAccountClusterRoleRuleList: list[ClusterRoleRuleSchema] = [
    ClusterRoleRuleSchema(apiGroups=[GroupVersion.group], resources=[{{ kind }}Plural], verbs=["get", "list", "watch"]),
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

    # TODO(user): your logic here

    # set the observed state of {{ kind }} object
    # patch.setdefault("status", {}).update({})

