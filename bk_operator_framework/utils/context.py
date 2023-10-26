import threading

_local = threading.local()


def set_trace_id(trace_id: str):
    """
    使用 CR 唯一的 UID作为Trace ID
    :param trace_id:
    :return:
    """
    _local.trace_id = trace_id


def get_trace_id() -> str:
    return getattr(_local, "trace_id", "UNKNOWN")
