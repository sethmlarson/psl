import os
import re

from setuptools import setup

with open(os.path.abspath("psl/__init__.py"), "r") as f:
    version = re.search(r"__version__\s+=\s+\"([\d.]+)\"", f.read()).group(1)

with open("README.md") as f:
    long_description = f.read()


setup(
    name="psl",
    version=version,
    description="Mozilla Public Suffix list as a Python package and updated daily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MPL-2.0",
    url="https://github.com/sethmlarson/psl",
    author="Seth Michael Larson",
    author_email="sethmichaellarson@gmail.com",
    packages=["psl"],
    package_dir={"psl": "psl"},
    package_data={"psl": ["psl.txt"]},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
    ],
)
