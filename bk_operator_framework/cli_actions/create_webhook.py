import sys

from bk_operator_framework.cli_actions import echo


def main():
    echo.warn("command[bof create webhook] not supported yet!")
    sys.exit(1)
