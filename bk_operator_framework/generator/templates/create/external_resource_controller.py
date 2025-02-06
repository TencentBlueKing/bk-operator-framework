import kopf
from bk_operator_framework.generator.schemas import RBACRule, GroupVersion

GROUP_VERSION = GroupVersion(group="{{ (group + '.' + domain).rstrip('.') }}", version="{{ version }}")
{{ kind | upper }}_PLURAL = "{{ plural }}"

RBAC_RULE_LIST: list[RBACRule] = [
    RBACRule(apiGroups=[GROUP_VERSION.group], resources=[{{ kind | upper }}_PLURAL], verbs=["get", "list", "watch"]),
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

    # TODO(user): your logic here

    # set the observed state of {{ kind }} object
    # patch.setdefault("status", {}).update({})

