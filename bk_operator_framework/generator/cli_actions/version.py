import importlib.metadata

from bk_operator_framework.generator.cli_actions import echo


def main() -> None:
    name, *_ = __name__.split(".")
    version = importlib.metadata.version(name)
    echo.info(f"bof version is {version}")
