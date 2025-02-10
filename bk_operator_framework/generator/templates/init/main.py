"""
CLI entry point, when used as a module: `python -m kopf` or `python -m bk_operator_framework`.

Useful for debugging in the IDEs (use the start-mode "Module", module "kopf" or "bk_operator_framework").
"""
from kopf import cli as kopf_cli
from bk_operator_framework.kits import kopf as bof_kopf

if __name__ == "__main__":
    bof_kopf.prepare_startup()

    kopf_cli.main()
