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
async def reconcile(spec, **kwargs):
    spec_obj = {{ kind }}Spec(**spec)
    print(f"Hello, {spec_obj.foo}")

    return {{ kind }}Status().model_dump()