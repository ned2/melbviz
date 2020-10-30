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

```
python3 -m pip install jupyter-repo2docker --user
```


### Creating the Docker Image

First clone the repository:

```
git clone https://github.com/ned2/melbviz.git
```

Then let's create Docker image from it. Please note that this will download a
fair bit of data, so you might not want to be using mobile data. The image
itself once installed is ~3GB.

```
repo2docker <path-to-cloned-repo> --no-run --image-name melbviz
```

### Running the Image

Find the ID of the image you just created:

```
docker image ls | grep r2d
```

Now run it:

```
docker run -p 8888:8888 -p 8050:8050 <image-id>
```

If all has worked, you should now be able to open up Jupyter Lab in your browser
at the following address: http://localhost:8888/lab. You will then need to copy
the security token displayed on your terminal into the dialogue box.

Once you have Jupyter Lab loaded, navigate to the `workshop` directory in the
directory tree and open up `workshop_part1.ipynb`.

You're now ready to start the workshop!
