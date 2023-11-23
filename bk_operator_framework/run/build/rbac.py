import copy
import os

import yaml

rbac_template_dict = {
    "service_account": {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {
            "namespace": "{{ .Release.Namespace }}",
            "name": "{{ .Values.serviceAccount.name }}",
        },
    },
    "cluster_role": {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRole",
        "metadata": {"name": "{{ .Values.appName }}-role-cluster"},
        "rules": [
            {
                "apiGroups": ["kopf.dev"],
                "resources": ["clusterkopfpeerings"],
                "verbs": ["list", "watch", "patch", "get"],
            },
            {
                "apiGroups": ["apiextensions.k8s.io"],
                "resources": ["customresourcedefinitions"],
                "verbs": ["list", "watch"],
            },
            {"apiGroups": [""], "resources": ["namespaces"], "verbs": ["list", "watch"]},
            {
                "apiGroups": ["admissionregistration.k8s.io"],
                "resources": ["validatingwebhookconfigurations", "mutatingwebhookconfigurations"],
                "verbs": ["create", "patch"],
            },
            {"apiGroups": [""], "resources": ["events"], "verbs": ["create"]},
            {"apiGroups": ["kopf.dev"], "resources": ["kopfexamples"], "verbs": ["list", "watch"]},
        ],
    },
    "cluster_role_binding": {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {"name": "{{ .Values.appName }}-rolebinding-cluster"},
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "{{ .Values.appName " "}}-role-cluster",
        },
        "subjects": [
            {
                "kind": "ServiceAccount",
                "name": "{{ .Values.serviceAccount.name }}",
                "namespace": "{{ .Release.Namespace }}",
            }
        ],
    },
    "role": {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "Role",
        "metadata": {
            "namespace": "{{ .Release.Namespace }}",
            "name": "{{ .Values.appName }}-role-namespaced",
        },
        "rules": [
            {"apiGroups": ["kopf.dev"], "resources": ["kopfpeerings"], "verbs": ["list", "watch", "patch", "get"]},
            {"apiGroups": [""], "resources": ["events"], "verbs": ["create"]},
            {"apiGroups": ["batch", "extensions"], "resources": ["jobs"], "verbs": ["create"]},
            {
                "apiGroups": ["admissionregistration.k8s.io"],
                "resources": ["validatingwebhookconfigurations", "mutatingwebhookconfigurations"],
                "verbs": ["create", "patch"],
            },
            {"apiGroups": ["kopf.dev"], "resources": ["kopfexamples"], "verbs": ["list", "watch", "patch"]},
        ],
    },
    "role_binding": {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
        "metadata": {
            "namespace": "{{ .Release.Namespace }}",
            "name": "{{ .Values.appName }}-rolebinding-namespaced",
        },
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "Role",
            "name": "{{ .Values.appName }}-role-namespaced",
        },
        "subjects": [{"kind": "ServiceAccount", "name": "{{ .Values.serviceAccount.name }}"}],
    },
}


def build_rbac_yaml(operator_cls, version_helm_charts_dir):
    template_helm_charts_dir = os.path.join(version_helm_charts_dir, "templates", "rbac")
    if not os.path.exists(template_helm_charts_dir):
        os.makedirs(template_helm_charts_dir)

    rbac_dict = copy.deepcopy(rbac_template_dict)

    rbac_dict.pop("role")
    rbac_dict.pop("role_binding")
    rbac_dict["cluster_role"]["rules"][-1]["resources"] = [operator_cls.Meta.plural]
    rbac_dict["cluster_role"]["rules"].append(
        {
            "apiGroups": [operator_cls.Meta.group],
            "resources": [operator_cls.Meta.plural],
            "verbs": ["get", "watch", "list", "create", "update", "patch", "delete"],
        }
    )
    rbac_dict["cluster_role"]["rules"].extend(operator_cls._get_rbac_schema()["extra_role_rules"])

    for rbac_file_name, rbac_data in rbac_dict.items():
        rbac_yaml_path = os.path.join(template_helm_charts_dir, "{}.yaml".format(rbac_file_name))
        with open(rbac_yaml_path, "w") as file:
            yaml.dump(rbac_data, file)
