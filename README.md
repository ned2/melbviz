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
* A workshop in the form of two Jupyter Notebooks that will take you on a
  dashboarding journey, going from initial discovery and data wrangling to
  deploying your completed Dashboard.

You can use Melbviz either through a pre-configured Docker image, or by
installing it into your local environment. If you are participating in a
workshop, then unless otherwise instructed, you want installation method `A`.


## Live Environment on Binder

This repo has been prepared to run on the wonderful
[Binder](https://mybinder.org/) service.

This link will spin up a notebook in JupyterLab with all relevant dependencies
installed and data downloaded ready to go for you to play around with.

https://mybinder.org/v2/gh/ned2/melbviz/HEAD?urlpath=lab%2Ftree%2Fnotebooks%2Finteractive_data_viz.ipynb


## Local Installation Instructions

To install Melbviz in your own environment (Ubuntu instructions only
sorry), follow the following steps:

Ubuntu system dependencies:
* Python 3.8+
* `libsnappy-dev`

```
sudo apt-get install libsnappy-dev
```

Create and activate a new virtual environment, then run:

```
pip install -e .
```

Documentation TODO:
* Getting the data
* Installing Jupyter Lab extensions 
