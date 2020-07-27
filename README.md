# Melbviz

Melbviz is a package for learning how to building sashboards in Python, using
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


## A: Workshop Instructions

These instructions will create a Docker image containing the full environment
required to complete the workshop. To follow them, you will first need to
install:

* [Docker installed](https://docs.docker.com/get-docker)
* [repo2docker](https://repo2docker.readthedocs.io/en/latest/install.html)

Depending on how you have Python setup, will either be able to install repo2docker 
using this command:

```
python3 -m pip install jupyter-repo2docker
```

...or you may need to perform a local install:

`python3 -m pip install jupyter-repo2docker --user`


### Creating the Docker Image

```
repo2docker https://github.com/ned2/melbviz --no-run --image-name melbviz
```

### Running the Image

Find the ID of the image you just created:

```
docker image ls | grep r2d
```

Now run it:

```
docker run -p 8888:8888 <image-id>
```

If all has worked, you should now be able to open up Jupyter Lab in your browser
at the following address: http://localhost:8888/lab. You will then need to copy
the security token displayed on your terminal into the dialogue box.

Once you have Jupyter Lab loaded, navigate to the `notebooks` directory in the
directory tree and open up `workshop_part1.ipynb`.

You're now ready to start the workshop!


## B: Local Installation Instructions

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
* Installing Node
* Installing Jupyter Lab extensions 
