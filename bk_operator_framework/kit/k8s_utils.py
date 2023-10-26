import logging
import os
import socket
import time

from kubernetes import client

logger = logging.getLogger("bk-operator")


def get_current_pod_ip():
    """
    获取当前pod ip
    :return:
    """

    return socket.gethostbyname(socket.gethostname())


def get_current_namespace():
    """
    获取当前Operator Server的命名空间
    :return:
    """
    return os.environ.get("OPERATOR_DEPLOY_NAMESPACE", "default")


def get_namespaced_cr_info(group, version, namespace, plural, name):
    """
    获取命名空间下的 CR 对象
    :param group:
    :param version:
    :param namespace:
    :param plural:
    :param name:
    :return:
    """
    custom_api = client.CustomObjectsApi()

    return custom_api.get_namespaced_custom_object(group, version, namespace, plural, name)


def get_cluster_cr_info(group, version, plural, name):
    """
    获取集群级别的 CR 对象
    :param group:
    :param version:
    :param plural:
    :param name:
    :return:
    """
    custom_api = client.CustomObjectsApi()
    return custom_api.get_cluster_custom_object(group, version, plural, name)


def patch_namespaced_cr_status(group, version, namespace, plural, name, status):
    """
    更新命名空间级别 CR 的 Status
    :param status:
    :param group:
    :param version:
    :param namespace:
    :param plural:
    :param name:
    :return:
    """
    logger.debug(f"start update {namespace} [{plural}.{group}/{version}: {name}] status")
    custom_api = client.CustomObjectsApi()

    for retry_tum in range(1, 5):
        try:
            current_cr = custom_api.get_namespaced_custom_object(group, version, namespace, plural, name)
            current_cr["status"] = status
            custom_api.patch_namespaced_custom_object(group, version, namespace, plural, name, body=current_cr)
        except client.exceptions.ApiException as e:
            if e.status == 409:
                logger.warning(
                    f"update {namespace}  [{plural}.{group}/{version}: {name}] status failed due to resource "
                    f"conflict, retry_num=[{retry_tum}] "
                )
                time.sleep(1)
            else:
                raise e

    logger.debug(f"update {namespace} [{plural}.{group}/{version}: {name}] status finished.")


def patch_cluster_cr_status(group, version, plural, name, status):
    """
    更新集群级别 CR 的 Status
    :param status:
    :param group:
    :param version:
    :param plural:
    :param name:
    :return:
    """
    logger.debug(f"start update cluster [{plural}.{group}/{version}: {name}] status")
    custom_api = client.CustomObjectsApi()

    for retry_tum in range(1, 5):
        try:
            current_cr = custom_api.get_cluster_custom_object(group, version, plural, name)

            current_cr["status"] = status
            custom_api.patch_cluster_custom_object(group, version, plural, name, body=current_cr)
        except client.exceptions.ApiException as e:
            if e.status == 409:
                logger.warning(
                    f"update cluster  [{plural}.{group}/{version}: {name}] status failed due to resource "
                    f"conflict, retry_num=[{retry_tum}] "
                )
                time.sleep(1)
            else:
                raise e

    logger.debug(f"update cluster [{plural}.{group}/{version}: {name}] status finished.")


def patch_namespaced_cr_annotations(group, version, namespace, plural, name, annotations):
    """
    更新 命名空间级别 CR 的 annotations
    :param annotations:
    :param group:
    :param version:
    :param namespace:
    :param plural:
    :param name:
    :return:
    """
    logger.debug(f"start update {namespace} [{plural}.{group}/{version}: {name}] annotations")
    custom_api = client.CustomObjectsApi()

    for retry_tum in range(1, 5):
        try:
            current_cr = custom_api.get_namespaced_custom_object(group, version, namespace, plural, name)
            raw_annotations = current_cr.get("metadata", {}).get("annotations", {})
            raw_annotations.update(annotations)
            custom_api.patch_namespaced_custom_object(group, version, namespace, plural, name, body=current_cr)
        except client.exceptions.ApiException as e:
            if e.status == 409:
                logger.warning(
                    f"update {namespace}  [{plural}.{group}/{version}: {name}] annotations failed due to resource "
                    f"conflict, retry_num=[{retry_tum}] "
                )
                time.sleep(1)
            else:
                raise e

    logger.debug(f"update {namespace} [{plural}.{group}/{version}: {name}] annotations finished.")


def patch_cluster_cr_annotations(group, version, plural, name, annotations):
    """
    更新 集群级别的 CR 的 annotations
    :param annotations:
    :param group:
    :param version:
    :param plural:
    :param name:
    :return:
    """
    logger.debug(f"start update cluster [{plural}.{group}/{version}: {name}] annotations")
    custom_api = client.CustomObjectsApi()

    for retry_tum in range(1, 5):
        try:
            current_cr = custom_api.get_cluster_custom_object(group, version, plural, name)
            raw_annotations = current_cr.get("metadata", {}).get("annotations", {})
            raw_annotations.update(annotations)
            custom_api.patch_cluster_custom_object(group, version, plural, name, body=current_cr)
        except client.exceptions.ApiException as e:
            if e.status == 409:
                logger.warning(
                    f"update cluster  [{plural}.{group}/{version}: {name}] annotations failed due to resource "
                    f"conflict, retry_num=[{retry_tum}] "
                )
                time.sleep(1)
            else:
                raise e

    logger.debug(f"update cluster [{plural}.{group}/{version}: {name}] annotations finished.")
