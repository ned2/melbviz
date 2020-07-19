import os

from setuptools import setup, find_packages


# Package meta-data.
NAME = "melbviz"
DESCRIPTION = "A library for building dashboards on the Melbourne City Council Pedestrian Counting dataset"

URL = "https://github.com/ned2/melbviz"
AUTHOR = "Ned Letcher"
AUTHOR_EMAIL = "ned at nedned dot net"
LICENSE = "Mozilla Public License 2.0"
REQUIRES_PYTHON = ">=3.8.0"
VERSION = "0.0.1"


# What packages are required for this module to be executed?
REQUIRED = ["pandas", "plotly", "dash", "ipython", "ipywidgets", "voila"]

# Optional Packages
EXTRAS = {
    "eda": ["jupyterlab", "visidata", "ptpython", "black", "jupyterlab-code-formatter"]
}

# get the absolute path to this file
here = os.path.abspath(os.path.dirname(__file__))


# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


# If VERSION not specified above, load the package"s __version__.py module as a
# dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, "src", "luncher", "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=about["__version__"],
    packages=find_packages("src"),
    package_dir={"": "src"},
)
