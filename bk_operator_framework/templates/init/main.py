"""
CLI entry point, when used as a module: `python -m kopf` or `python -m bk_operator_framework`.

Useful for debugging in the IDEs (use the start-mode "Module", module "kopf" or "bk_operator_framework").
"""

from kopf import cli as kopf_cli
from bk_operator_framework.core import runtime as bof_runtime
import internal

if __name__ == "__main__":
    bof_runtime.load_kube_config()
    bof_runtime.discover_controllers(internal)

    kopf_cli.main()
