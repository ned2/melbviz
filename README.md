# Melbviz

Melbviz is a package for learning how to building dashboards in Python, using
the [Dash library](plotly/dash), and also for learning about Pedestrian traffic
in the central business district of Melbourne, Australia. The package is
designed around analysing the Melbourne City Council [Pedestrian Counting System
dataset](https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-2009-to-Present-counts-/b2ak-trbp).

The project consists of:
* A python package, `melbviz`, that contains the ingredients for building out
  your own interactive interfaces for exploring Melbourne CBD pedestrian traffic
  using [Dash](plotly/dash), a library for building analytic web apps.
* A collection of Jupyter Notebooks for working with the Melbourne pedestrian datasets.

You can use Melbviz either through the live environment on Binder, or by
installing it into your local environment. If you are participating in a
workshop, then unless otherwise instructed, you want to use the Binder method.

## Jupyter Notebooks

These notebooks are found in the `notebooks` directory. The
`talk_data_viz.ipynb` requires the use of Jupyter Notebook classic to view the
RISE presentation. It is recommended to use JupyterLab for the remaining
notebooks.

* `talk_data_viz.ipynb`: A presentation on why we do data visualisation that
  uses the [RISE](https://rise.readthedocs.io) package
* `interactive_data_viz.ipynb`: A workshop that goes through the use of the
  Plotly visualisation package and the ipywidgets package, for doing interactice
  data visualisation.
* `workshop_dashboards1.ipynb` and `workshop_dashboards1.ipyn`: A workshop in
  two parts that will take you on a dashboarding journey, going from initial
  discovery and data wrangling to deploying your completed Dash dashboard.
  

## Live Environment on Binder

This repo has been prepared to run on the wonderful
[Binder](https://mybinder.org/) service.

This link will spin up a notebook in JupyterLab with all relevant dependencies
installed and data downloaded ready to go for you to play around with.

https://mybinder.org/v2/gh/ned2/melbviz/HEAD?urlpath=lab%2Ftree%2Fnotebooks%2Finteractive_data_viz.ipynb


## Local Installation Instructions

To install Melbviz in your own environment (Ubuntu instructions only sorry),
follow the following steps:

Ubuntu system dependencies:
* Python 3.8+
* `libsnappy-dev`

```
sudo apt-get install libsnappy-dev
```

Create and activate a new virtual environment, then run, the following
commands. Or, if you use [pyenv](https://github.com/pyenv/pyenv), you can run
the `make-env.sh` to do all of this in one step (see script to change Python
version or venv name).


```
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
```

Download and prep the data:

    ./get-data.sh
