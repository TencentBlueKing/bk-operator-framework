import functools
import logging

logger = logging.getLogger("bk-operator")


def handler(handler_type: str, **handler_kwargs):
    def register_handler(handler_fn):
        @functools.wraps(handler_fn)
        def raw_handler(*args, **kwargs):
            return handler_fn(*args, **kwargs)

        raw_handler.handler_type = handler_type
        raw_handler.handler_kwargs = handler_kwargs
        raw_handler.version = None
        return raw_handler

    return register_handler
