import logging

from bk_operator_framework.utils import context


class TraceIDInjectFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.trace_id = context.get_trace_id()
        return True


def init_logger(level=logging.INFO):
    logging.basicConfig(level=level)

    logger = logging.getLogger("bk-operator")
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s %(levelname)s/%(name)s.%(trace_id)s]: %(message)s")
    handler.setFormatter(formatter)
    handler.addFilter(TraceIDInjectFilter())
    logger.addHandler(handler)

    kopf_logger = logging.getLogger("kopf")
    kopf_logger.propagate = False
    kopf_handler = logging.StreamHandler()
    kopf_formatter = logging.Formatter("[%(asctime)s %(levelname)s/%(name)s]: %(message)s")
    kopf_handler.setFormatter(kopf_formatter)
    kopf_logger.addHandler(kopf_handler)
