"""
The package for working with Opem Media XML exports
"""

from os import path
from setuptools import setup, find_namespace_packages

NAMESPACE = "cro"
PACKAGE_PATH = f"{NAMESPACE}.rundown"
PACKAGE_NAME = f"{NAMESPACE}.rundown"

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "LICENSE"), encoding="utf-8") as f:
    LICENSE = f.read()

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=f"{PACKAGE_NAME}",
    version="0.1.0",
    author="Czech Radio",
    author_email="david.landa@rozhlas.cz",
    description=__doc__,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=[f"{NAMESPACE}.*"]),
    install_requires=[
        "xlrd",
        "tqdm",
        "pylev3",
        "loguru",
        "pandas",
        "pandera",
        "openpyxl",
        "progress",
        "psycopg2",
    ],
    extras_require={
        "test": ["pytest"],
        "lint": ["black", "pylint", "flake8", "mypy"],
        "docs": ["pdoc3"],
    },
    entry_points={
        "console_scripts": [
            f"{PACKAGE_NAME}.parse={PACKAGE_PATH}.__main__:main", # todo
            f"{PACKAGE_NAME}.clean={PACKAGE_PATH}.__main__:main",
        ]
    },
    zip_safe=False,
)
