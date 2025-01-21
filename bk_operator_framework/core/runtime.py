import logging
import os
import pkgutil
import sys
import typing
from importlib import import_module

import kopf.on
from kubernetes import config

logger = logging.getLogger("bof.core.runtime")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(name)-20.20s [%(levelname)-8.8s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def _list_all_modules(module_dir: str, sub_dir: str = None) -> typing.List[str]:
    modules = []
    for _, name, is_pkg in pkgutil.iter_modules([module_dir]):
        if name.startswith("_"):
            continue
        module = name if sub_dir is None else "{}.{}".format(sub_dir, name)
        if is_pkg:
            modules += _list_all_modules(os.path.join(module_dir, name), module)
        else:
            modules.append(module)
    return modules


def load_server(server_type):
    logger.info(f"server_type is {server_type}")
    if server_type not in {"controller", "webhook"}:
        raise RuntimeError(f"The server type[{server_type}] is invalid")
    module = import_module(f"internal.{server_type}")
    module_dir = module.__path__[0]
    sys.path_importer_cache.pop(module_dir, None)
    modules = _list_all_modules(module_dir)
    for name in modules:
        module_path = "{}.{}".format(module.__name__, name)
        import_module(module_path)
        logger.info(f"{module_path} has been loaded")

    if server_type == "webhook":

        @kopf.on.startup()
        def configure(settings: kopf.OperatorSettings, **_):
            # Assuming that the configuration is done manually:
            if "KUBERNETES_SERVICE_HOST" in os.environ:
                webhook_kwargs = {
                    "port": int(os.getenv("WEBHOOK_PORT", 8443)),
                    "certfile": os.getenv("WEBHOOK_TLS_CERT_PATH", "/workspace/etc/certs/tls.crt"),
                    "pkeyfile": os.getenv("WEBHOOK_TLS_KEY_PATH", "/workspace/etc/certs/tls.key"),
                }
            else:
                webhook_kwargs = {
                    "port": int(os.getenv("WEBHOOK_PORT", 8443)),
                }

            settings.admission.server = kopf.WebhookServer(**webhook_kwargs)


def load_kube_config():
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
