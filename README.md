# Video to frames processing with Pachyderm

This project demonstrates how to use Pachyderm for distributed video processing. For this tutorial, we'll upload  Seals.mpg, a 3 second video of a seal, to a input [Pachyderm repo](https://docs.pachyderm.com/latest/concepts/data-concepts/repo/). Next we'll develop a [Pachderm pipeline](https://docs.pachyderm.com/latest/how-tos/developer-workflow/working-with-pipelines/) which will transform the video into frames and output 76 jpg images in an output Pachyderm repo. 

## Important Notes
This example of video processing mirrors was based off the following [Beginner Tutorial](https://docs.pachyderm.com/latest/getting-started/beginner-tutorial/). Use that tutorial as a resource for a how-to guide on how this project was created. 

This example is very minimal as it processes a single video, which doesn't serve to highlight the true power of Pachyderm. Pachyderm shines in the instance where users need to process thousands of videos and organize their frame outputs with parallel processing. To learn about how to extend this example into a more real-world use case please pay attention to the following documentation: 
- [Glob patters](https://docs.pachyderm.com/latest/concepts/pipeline-concepts/datum/glob-pattern/#glob-pattern)
- [Parallelism](https://docs.pachyderm.com/latest/concepts/advanced-concepts/distributed-computing/)

Additionally, please reach out for help on the [Pachyderm Slack Community](https://www.pachyderm.com/slack/). 

## File Overview
- [frames.py](./frames.py) uses OpenCV, a popular Python library for computer vision, to split a video into frames. This code was largely borrowed from [this repo](https://github.com/vfdev-5/Video2Frames).
- [fames.json](./frames.json) creates the Pachyderm pipeline for this distribued video processing.  
- The [Dockerfile](./Dockerfile) was used to create the [anaisdg/opencv](https://hub.docker.com/repository/docker/anaisdg/opencv/general) image which is used to process each video. The anaisdg/opencv image uses the [jjanzic/docker-python3-opencv](https://hub.docker.com/r/jjanzic/docker-python3-opencv/tags) image which is based off of the official Python 3 image and has an additon of OpenCV. This Dockerfile is not required to run the project, but serves as an example for those wanting to build their own project and pipeline. 
- [frames_solo.py](./frames_solo.py) and [requirements.txt](./requirements.txt) were used during the development of this project to ensure that the video processing script was successful. They are not required to run this project. 

## Prerequisites 
1. Install and deploy Pachyderm community edition locally. Follow this [Getting Started](https://docs.pachyderm.com/latest/getting_started/) guide to get up and running. 
2. Install [Docker Desktop](https://docs.pachyderm.com/latest/getting-started/local-installation/#using-kubernetes-on-docker-desktop) locally. 
3. Install the [Pachyderm CLI](https://docs.pachyderm.com/latest/getting-started/local-installation/#install-pachctl)
4. Install [Kubernetes CLI](https://kubernetes.io/docs/tasks/tools/)

## Execute 
1. Create an input repo with `pachctl create repo videos`.
2. Verify that the repo creation was successful with `pachctl list repo` or through the UI. 
3. Add [Seal.mpg](./Seal.mpg) to the input repo with `pachctl put file videos@master:Seal.mpg -f ./Seal.mpg`
4. Verify that the data addition to videos was succesful with `pachctl list file videos@master` or through the UI. 
5. Create a pipeline with `pachctl create pipeline -f frames.json`. 
6. Verify that the distributed video processing and output repo, images, was successful with `pachctl list job` or thorugh the UI. 
   
## Debugging Tips 
1. View the logs for each job in the UI or with
2. Run `kubectl get pods` to view the status of each pod. 
3. Run `pachctl list pipeline` to view the status of each pipeline. 
