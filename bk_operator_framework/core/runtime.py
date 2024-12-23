import logging
import os
import pkgutil
import sys
import typing
from importlib import import_module

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


def discover_controllers(module):
    module_dir = module.__path__[0]
    sys.path_importer_cache.pop(module_dir, None)
    modules = _list_all_modules(module_dir)
    for name in modules:
        module_path = "{}.{}".format(module.__name__, name)
        import_module(module_path)
        logger.info(f"Discovered {module_path}")


def load_kube_config():
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
