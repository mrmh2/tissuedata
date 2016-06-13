# tissuedata

## Introduction

This repository provides data structures and code for working with images of 
whole tissue data, comprised of individual cells

### Reading images/data and printing JSON

To run the script, pass a segmented image file, microscope metadata, and the HAS file:

    python tissuedata/jsoner.py data/T06.png data/T06.txt data/T06.has

or point the scrape_data.sh shell script at a data directory

    sh scrape_data.sh /path/to/data /path/to/output

this will create a .json file for each timepoint in the experiment

## Docker

This image analysis project has been setup to take advantage of a technology
known as Docker.

This means that you will need to:

1. Download and install the [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
2. Build a docker image.

Before you can run the image analysis in a docker container.


## Build a Docker image

Before you can run your analysis you need to build your docker image.  Once you
have built the docker image you should not need to do this step again.

A docker image is basically a binary blob that contains all the dependencies
required for the analysis scripts. In other words the docker image has got no
relation to the types of images that we want to analyse, it is simply a
technology that we use to make it easier to run the analysis scripts.

```
$ cd docker
$ bash build_docker_image.sh
$ cd ..
```

## Run the image analysis in a Docker container

The image analysis will be run in a Docker container.  The script
``run_docker_container.sh`` will drop you into an interactive Docker session.

```
$ bash run_docker_container.sh
[root@048bd4bd961c /]#
```

Now you can run the image analysis.

```
[root@048bd4bd961c /]# python scripts/analysis.py data/ output/

```
## Requirements

needs 'freeimage' backend

```
brew install freeimage
```