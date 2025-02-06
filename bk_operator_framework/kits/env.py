import os

from kubernetes import config


def running_in_cluster() -> bool:
    """
    Is the current operating environment in the k8s cluster?
    :return:
    """
    return "KUBERNETES_SERVICE_HOST" in os.environ


def load_auth_and_cluster_info() -> None:
    """
    Loads authentication and cluster information
    :return:
    """
    if running_in_cluster():
        config.load_incluster_config()
    else:
        config.load_kube_config()
