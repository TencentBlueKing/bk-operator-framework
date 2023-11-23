import logging

from bk_operator_framework.run.dev import run_dev
from bk_operator_framework.utils.log import init_logger

if __name__ == "__main__":
    init_logger(logging.INFO)
    run_dev()
