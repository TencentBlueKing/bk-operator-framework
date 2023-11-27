from setuptools import find_packages, setup

setup(
    name="bk_operator_framework",
    version="0.4.6",
    packages=find_packages(include=["bk_operator_framework", "bk_operator_framework.*"]),
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "bof=bk_operator_framework.run.command_line:main",
        ],
    },
    install_requires=[
        "kopf==1.36.1",
        "kubernetes==26.1.0",
        "cryptography>=3.0.0,<=4.0.0",
        "pydantic>=2.0,<3.0",
        "PyYAML>=5.0,<7.0",
    ],
)
