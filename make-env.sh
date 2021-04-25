#!/usr/bin/env bash

PYTHON=3.9.4
VENV=melbviz

pyenv virtualenv ${PYTHON} ${VENV}
export PYENV_VERSION=${VENV}

pip install -U pip wheel
pip install -r requirements.txt
pip install -e .

jupyter labextension install @pyviz/jupyterlab_pyviz
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget
jupyter labextension install jupyterlab-plotly
jupyter labextension install @ryantam626/jupyterlab_code_formatter
jupyter nbextension install --py hide_code
jupyter nbextension enable --py hide_code
jupyter serverextension enable --py hide_code

unset PYENV_VERSION
