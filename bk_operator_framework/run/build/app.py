import copy
import os

import yaml

app_template_dict = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "{{ .Chart.Name }}-deployment"},
    "spec": {
        "replicas": 1,
        "selector": {"matchLabels": {"app": "{{ .Values.appName }}"}},
        "template": {
            "metadata": {"labels": {"app": "{{ .Values.appName }}"}},
            "spec": {
                "serviceAccountName": "{{ .Values.serviceAccount.name }}",
                "containers": [
                    {
                        "name": "{{ .Values.appName }}-app",
                        "image": "{{ .Values.image.repository }}:{{ .Values.image.tag }}",
                        "command": ["bof", "run", "server", "version"],
                        "env": [{"name": "OPERATOR_DEPLOY_NAMESPACE", "value": "{{ .Release.Namespace }}"}],
                    }
                ],
            },
        },
    },
}


def build_app_yaml(operator_cls, version_helm_charts_dir):
    template_helm_charts_dir = os.path.join(version_helm_charts_dir, "templates", "app")
    if not os.path.exists(template_helm_charts_dir):
        os.makedirs(template_helm_charts_dir)

    chart_yaml_path = os.path.join(template_helm_charts_dir, "app.yaml")
    app_dict = copy.deepcopy(app_template_dict)
    app_dict["spec"]["template"]["spec"]["containers"][0]["command"][-1] = operator_cls.Meta.version
    for env_key in operator_cls.CUSTOM_ENVIRONMENT_KEY:
        app_dict["spec"]["template"]["spec"]["containers"][0]["env"].append(
            {"name": env_key, "value": f"{{{{ .Values.env.{env_key} }}}}"}
        )

    with open(chart_yaml_path, "w") as file:
        yaml.dump(app_dict, file)
