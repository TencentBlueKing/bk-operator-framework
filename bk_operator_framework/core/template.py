import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader

from bk_operator_framework.cli_actions import echo

TEMPLATE_ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
WORK_DIR = os.getcwd()


def init_project_dir():
    init_template_dir = os.path.join(TEMPLATE_ROOT_DIR, "init")
    for root, dirs, files in os.walk(init_template_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(WORK_DIR, os.path.relpath(src_file, init_template_dir))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)


def create_file(target_relative_path, template_relative_path, render_vars):
    env = Environment(loader=FileSystemLoader(TEMPLATE_ROOT_DIR))
    template = env.get_template(template_relative_path)
    rendered_content = template.render(**render_vars)
    target_file = os.path.join(WORK_DIR, target_relative_path)
    with open(target_file, "w", encoding="utf-8") as file:
        file.write(rendered_content)


def create_resource(group, version, kind, singular, plural, domain):
    echo.info(f"api/{group}/{version}/group_version.py")
    echo.info(f"api/{group}/{version}/{singular}_schemas.py")

    resource_dir = os.path.join(WORK_DIR, "api", group, version)
    os.makedirs(resource_dir, exist_ok=True)

    group_init_path = os.path.join(WORK_DIR, "api", group, "__init__.py")
    open(group_init_path, "a").close()

    version_init_path = os.path.join(resource_dir, "__init__.py")
    open(version_init_path, "a").close()

    group_version_file_path = os.path.join(resource_dir, "group_version.py")
    if not os.path.exists(group_version_file_path):
        group_version_kwargs = {
            "target_relative_path": os.path.relpath(group_version_file_path, os.getcwd()),
            "template_relative_path": os.path.join("create", "group_version.py"),
            "render_vars": {"group": f"{group}.{domain}", "version": version},
        }
        create_file(**group_version_kwargs)

    resource_schemas_path = os.path.join(resource_dir, f"{singular}_schemas.py")
    if os.path.exists(resource_schemas_path):
        echo.fata(f"failed to create api/{group}/{version}/{singular}_schemas.py: file already exists")
        sys.exit(1)

    resource_schemas_kwargs = {
        "target_relative_path": os.path.relpath(resource_schemas_path, os.getcwd()),
        "template_relative_path": os.path.join("create", "resource_schemas.py"),
        "render_vars": {"kind": kind, "plural": plural, "singular": singular},
    }
    create_file(**resource_schemas_kwargs)

    return resource_dir


def create_controller(group, version, kind, singular, plural):
    echo.info(f"internal/controller/{singular}_controller.py")

    controller_dir = os.path.join(WORK_DIR, "internal", "controller")
    os.makedirs(controller_dir, exist_ok=True)

    controller_init_path = os.path.join(controller_dir, "__init__.py")
    open(controller_init_path, "a").close()

    resource_controller_path = os.path.join(controller_dir, f"{singular}_controller.py")
    if os.path.exists(resource_controller_path):
        echo.fata(f"failed to create internal/controller/{singular}_controller.py: file already exists")
        sys.exit(1)

    resource_controller_kwargs = {
        "target_relative_path": os.path.relpath(resource_controller_path, os.getcwd()),
        "template_relative_path": os.path.join("create", "resource_controller.py"),
        "render_vars": {
            "kind": kind,
            "plural": plural,
            "singular": singular,
            "group": group,
            "version": version,
        },
    }
    create_file(**resource_controller_kwargs)

    return controller_dir
