import argparse
import logging
import os
import sys

from bk_operator_framework.run.build.tools import build
from bk_operator_framework.run.dev import run_dev
from bk_operator_framework.run.init.tools import init_operator_example
from bk_operator_framework.run.server import run_server
from bk_operator_framework.utils.log import init_logger


def main():
    sys.path.append(os.getcwd())

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialization development template example")
    init_parser.add_argument("operator_project_name", help="Initialized operator project name")

    # build command
    build_parser = subparsers.add_parser(
        "build", help="Build the helm package according to the definition of operator class"
    )
    build_parser.add_argument(
        "-t",
        "--target_string",
        default="docker_hub_username/repo:latest",
        help="Set the target build stage to build, eg. <docker_hub_username>/<repository_name>:<tag>",
    )
    build_parser.add_argument("--skip-image", action="store_true", help="Skip docker build to build image>")
    build_parser.add_argument("--push-image", action="store_true", help="push image to docker hub")

    # run command
    run_parser = subparsers.add_parser("run", help="Run subcommands: dev or server")
    run_subparsers = run_parser.add_subparsers(dest="subcommand")

    # run dev command
    run_dev_parser = run_subparsers.add_parser("dev", help="Local development and debugging")
    run_dev_parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    run_dev_parser.add_argument("-f", "--config_file", help="kubectl configuration file")
    run_dev_parser.add_argument("-c", "--context", help="kubectl configuration context")

    # run server command
    run_server_parser = run_subparsers.add_parser("server", help="Production environment service starts and runs")
    run_server_parser.add_argument("version", help="Version of the service to run")

    args = parser.parse_args()

    if args.command == "init":
        operator_project_name = args.operator_project_name
        init_operator_example(operator_project_name)

    if args.command == "build":
        build_kwargs = {
            "target_string": args.target_string,
            "skip_image": args.skip_image,
            "push_image": args.push_image,
        }
        build(**build_kwargs)

    if args.command == "run":
        if args.subcommand == "server":
            init_logger(logging.INFO)
            version = args.version
            run_server(version)

        if args.subcommand == "dev":
            if args.debug:
                init_logger(logging.DEBUG)
            else:
                init_logger(logging.INFO)
            dev_kwargs = {"config_file": args.config_file, "context": args.context}
            run_dev(**dev_kwargs)


if __name__ == "__main__":
    main()
