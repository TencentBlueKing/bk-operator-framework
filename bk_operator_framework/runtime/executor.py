import logging
import threading

import kopf

from bk_operator_framework.hub.operator import OperatorHub
from bk_operator_framework.utils import context

logger = logging.getLogger("bk-operator")


class OperatorHandlerExecutor:
    def __init__(self, handler_fn):
        self.handler_fn = handler_fn
        self.handler_kwargs = handler_fn.handler_kwargs
        self.handler_type = handler_fn.handler_type

    def request_handler(self, *args, **kwargs):
        self.handler_fn = self.handler_fn.__func__
        thread = threading.Thread(target=self.execute, kwargs=kwargs)
        thread.start()

    def execute(self, *args, **kwargs):
        logger.info(f"Handler {self.handler_fn} is invoked.")

        # 获取 CR 的 UID 作为Trace ID
        cur_cr_uid = kwargs.get("body", {}).get("metadata", {}).get("uid", "UNKNOWN")
        context.set_trace_id(cur_cr_uid)

        operator_cls = OperatorHub.all_versions().get(self.handler_fn.version)
        if not operator_cls:
            raise RuntimeError(
                "operator definition error, module [{}] only one Operator class is allowed to be defined".format(
                    self.handler_fn.__module__
                )
            )

        try:
            operator_ins = operator_cls(*args, **kwargs)
            result = self.handler_fn(operator_ins, *args, **kwargs)
        except Exception as e:
            logger.exception(e)
            raise kopf.PermanentError(f"Handler {self.handler_fn} error.")

        logger.info(f"Handler {self.handler_fn} succeeded.")
        return result
