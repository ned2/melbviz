#!/usr/bin/env bash

PYTHON=3.8.6
VENV=melbviz

pyenv virtualenv ${PYTHON} ${VENV}
export PYENV_VERSION=${VENV}

pip install -U pip wheel pip-tools
pip install -r requirements.txt
pip install -e .

jupyter labextension install @pyviz/jupyterlab_pyviz
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget
jupyter labextension install jupyterlab-plotly
jupyter labextension install @ryantam626/jupyterlab_code_formatter

unset PYENV_VERSION
