from bk_operator_framework.generator.cli_actions import echo

__version__ = "1.0.0"


def main():
    echo.info(f"bof version is {__version__}")
