import os
import shutil


def init_operator_example(operator_project_name):
    work_dir = os.getcwd()
    project_base_dir = os.path.join(work_dir, operator_project_name)
    if not os.path.exists(project_base_dir):
        os.makedirs(project_base_dir)
    else:
        raise RuntimeError("project[{}] already exists, please check!!!".format(operator_project_name))

    module_dir = os.path.dirname(__file__)
    template_dir = os.path.join(module_dir, "templates")
    for filename in os.listdir(template_dir):
        src_path = os.path.join(template_dir, filename)
        dst_path = os.path.join(project_base_dir, filename)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
    print("Your Operator Project [{}] has been successfully initialized".format(operator_project_name))
