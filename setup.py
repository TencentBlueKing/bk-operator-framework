from setuptools import find_packages, setup

setup(
    name="bk_operator_framework",
    version="1.0.0",
    packages=find_packages(include=["bk_operator_framework", "bk_operator_framework.*"]),
    include_package_data=True,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "bof=bk_operator_framework.cli:bof",
        ],
    },
    install_requires=[
        "click==8.1.7",
        "Jinja2===3.1.4",
        "pydantic==2.10.3",
        "PyYAML==6.0.2",
        "ruamel.yaml==0.18.6",
        "semver==3.0.2",
        "kopf==1.37.4",
        "kubernetes==31.0.0",
    ],
)
