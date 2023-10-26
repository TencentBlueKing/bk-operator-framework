from importlib import import_module

import kopf
from kubernetes import config

from bk_operator_framework.hub.operator import OperatorHub
from bk_operator_framework.runtime.executor import OperatorHandlerExecutor
from bk_operator_framework.utils.module_load import discover_operators


def run_dev(config_file=None, context=None):
    discover_operators(import_module("bk_operator.versions"))
    config.load_kube_config(config_file=config_file, context=context)
    for _, operator_cls in OperatorHub.all_versions().items():
        for handler in operator_cls.get_handler_list():
            handler_executor = OperatorHandlerExecutor(handler)
            getattr(kopf.on, handler_executor.handler_type)(**handler_executor.handler_kwargs)(handler_executor.execute)

    kopf.run(clusterwide=True)
