# Dockerizing Scripts for the GBDX Platform
These instructions walk through the process of taking a simple python script that calculates NDBI from Landsat imagery and creating a docker container that is ready to register as a task on the GBDX platform. Before running through this exercise, make sure that you have a working [DockerHub account] (https://hub.docker.com), and have downloaded [Docker Quickstart] (https://www.docker.com/products/docker-toolbox).
______
## The Goal
The objective of this example is to make a docker container for a script that creatse a raster of NDBI for an input Landsat image. Docker containers are like very lightweight virtual machines. They contain the script you choose to run, and have all of the libraries necessary to run it installed as part of the container. 

Making docker containers can seem confusing when you've never worked with them before. So, to help you understand why we're doing the steps listed below, we will first become familiar with the final product.
### How to pull and access our pre-made docker container
1. Open Docker Quickstart. From your working directory, create a directory called "DockerExample" or similar, then move into that directory.
2. Pull the docker image from DockerHub by typing:
  `docker pull mgraber/examplendbi`
3. Run the docker image. To do this, type: `docker run -it mgraber/examplendbi bash` This command starts the docker image you just pulled. At this point, you should be able to use `ls` and `cd` commands to explore the contents of the docker container. The directory *built_up* is where the script lives. Check to make sure you can see *justNDBI.py* within this directory.


_______   
Now that you know what we're trying to accomplish, let's go back to the very beginning. As a GBDX user, you may have some already-written scripts or algorithms that you'd like to turn into tasks on the platform. (While our example uses a python script, docker containers can wrap scripts written in other languages, too.) The way the platform treats input/output is a little different than you would treat it by running your script on your local machine. To get our script ready for the platform, we are going to have to make a few modifications.

## Step One: Getting Your Script Ready
At this point, please refer to the script simpleNBDI.py in this repository.

This script looks in a specified directory for images with the suffix *'B5.TIF.ovr'*, and *'B6.TIF.ovr'*. It extracts the size, projection, and resolution from one of these rasters to serve as a template for the output raster. The script then opens bands 5 and 6, which correspond with NIR and SWIR data respectively. By scanning through the image line-by-line, the script then calculated NDBI for each pixel, and ultimately writes the output to a raster file with the suffix *_NDBI.TIF*.

There are a few key modifications we need to make to this script for it to work on the platform.

1. To your import statements, add `import json` and `import os`
2. On the GBDX platform, input data is retrieved from S3 locations the user specifies in their workflow. Our script is relatively simple, and only has one input. We will call it *'image'*. Remember the name you give your inputs, since we will have to keep them consistent when we register the task on the platform. If we were to run our script as a task on the platform (our ultimate goal!), the platform would take the data in the s3 location we specify as the *image* input, and move it to a directory called *'/mnt/work/input/image'*. To account for this, change the input path name in line 7 of *simpleNDBI.py* to `filepath = "/mnt/work/input/image/"`
3. Were we to run simpleNDBI.py on our local machine, it would create the output raster in the directory where we run it from. But docker containers are a little more complicated. After a task runs, the container goes away, along with everything in it! To actually retrieve our output, we need to create an output directory and specify an output file. This allows the platform to find the output from the task. Then, we can link our fancy new NDBI task with the task called StagetoS3 in order to retrieve our newly created information layer. Let's further modify simpleNDBI.py by adding the following after line 12.

  ```
  os.makedirs("/mnt/work/output/output")
  os.chdir("/mnt/work/output/output")
  id = get_rast[0].split("/")[-1].split("_")[0]
  outfile = ("/mnt/work/output/output/" + id + "_NDBI.TIF")
  ```
  
4. Lastly, tasks require statusfiles. For the sake of this example, we are going to create a really simple status to add to our script. At the very end of simpleNDBI.py, add the following.
  ```
  status = {}
  status['status'] = 'Success'
  status['reason'] = "It worked!"
  ```
Note that this status is sort of misleading. The script simply has to make it through to the last line in order to "succeed." While developing your task, be sure to check the output to verify that it *actually* succeeded.
Like in the previous step, we need to put this output somewhere. To do so, add these lines to the end of *simpleNDBI.py*

  ```
  with open('/mnt/work/status.json', 'w') as statusfile:
          json.dump(status,statusfile)
  ```

5. EXTRA CREDIT: Our script only takes a file as an input. It is common for tasks to also require input strings, though. The way the platform handles string inputs is by storing them in a JSON file called *ports.json*. Like the file inputs, *ports.json* is stored in a directory called */mnt/work/input/*. Let's modify our script to take in a string. For the sake of the example, we will pretend our task requires an input called *message*. The script then uses the string associated with the input name *message* as the status reason. To do this, first modify what you wrote in the previous step to say:

  ```
  status = {}
  status['status'] = 'Success'
  status['reason'] = message

  ```
In order to extract our message from ports.json, we need to add the following to our script, in a place prior to the statusfile creation:
  ```
  with open('/mnt/work/input/ports.json') as portsfile:
      ports_js = json.load(portsfile)
  message= ports_js['message']
  ```
This will read in our string from the JSON file that the platform creates so we are able to use it in the script.

As of now, your script should be docker-ready! A script with the modifications listed above is in this repository as *justNDBI.py*

##Step Two: Creating Your Dockerfile
Next, we will write a dockerfile. This file contains the instructions that docker uses to create your container. This is everything from installing python and necessary libraries to adding and running your script. Before we start, create a directory locally called *NDBIExample*. Within this directory, make another directory called *bin*. This is where we will put all of the code that will be included in the docker container. For this example, this is only the script *justNDBI.py*. Place a copy of *justNDBI.py* inside *bin*. 

From the command line, move back one level to *NDBIExample*. This is where we will make the Dockerfile. Type `nano Dockerfile` to open a blank document. (Or whatever text editor you want to use in place of nano.) We will go through the anatomy of a Dockerfile as we write one.

1. The first line of a Dockerfile gets the OS to be used in the Docker container. Type: `FROM ubuntu:14.04`

2. Next, we will make a directory within to docker container to place all of our code. Making, changing, and copying directories in a Dockerfile uses the same commands as doing so from the command line, preceeded by the word 'RUN'. In line 2, type: `RUN mkdir /built_up`

3. Now we will run `apt-get update` and `apt-get install` in order to install python and relevant libraries. You are essentially giving Docker the instructions to mimic what you'd do to install libraries through your computer's command line. For this script, we need both GDAL and scipy in addition to the standard python libraries. Type the following:
  ```
  RUN apt-get update && apt-get -y install\
     python \
     build-essential\
     python-software-properties\
     software-properties-common\
     python-pip\
     python-scipy\
     python-dev\
     gdal-bin\
     python-gdal\
     libgdal-dev
  ```
4. We also need to `pip install` GDAL. Type: `RUN pip install gdal`

5. Next, we will add our code. Since it is all nicely organized in *bin*, we only need to type: `ADD ./bin /built_up` 

6. Finally, we will add the command that runs our code. Type: `CMD python /built_up/justNDBI.py`

Exit nano to save your Dockerfile.

## Step Three: Setting Up Your Docker Repository
We will make our docker container locally before pushing it to DockerHub. To keep naming conventions consistent, though, let's set up the repository where the conatiner will ultimately go now.
1. Go to [DockerHub](hub.docker.com) and sign in.

2. Click *Create/Create Repository*

3. Make a repository called *examplendbi*

4. Next, we need to add some collaborators. This will let the platform interact with your docker container once you push it to DockerHub. Go to *Add Collaborators* and add: *tdgpbuild*, *tdgpdeploy*, and *tdgplatform*.

##Step Four: Building Your Docker Container
Return to the terminal window running docker. Make sure you are still in the *NDBIExample* directory where your Dockerfile is. To build your Dockerfile, type: `docker build -t yourDockerUsername/examplendbi .`  Building your docker container will take a few minutes the first time through. If you change your script or Dockerfile and need to rebuild, the subsequent times will be faster, since Docker builds things in layers.

##Step Five: Running Your Container and Testing Locally
Before running your newly-created Docker container, let's make sure it built correctly. To see your Docker images, type: `docker images`. You should see one labeled *yourDockerUsername/examplendbi*. If so, you're ready to run and test!

Running your docker container locally is the same process we did with the pre-made container at the very beginning of this exercise. We will introduce another step to this process, though. In order to test your Docker conatiner before registering a task on the platform, you will need to mount some input data in a way that mimics the way the platform moves files around. Essentially, you are going to pretend to be the platform. We will use the two Landsat images included in this repository as a test strip. First, we need to move the images to the local directory called *NDBIExample/data*. When the platform moves input files around, it puts it in 'directories' with the same name as the input. In our case, the input images would be placed in a 'directory' called *image*. Let's mimic this by creating a local directory *image* within the *NDBIExample/data* folder, and moving our Landsat rasters into it. The only other input for this example is our string, which is stored as *message*. To mimic the platform's treatment of strings, we are now going to create a file *ports.json* within *NDBIExample/data*. It will look like this:

  ```
  {
  "message":"This is my message!"
  }
  ```
Now, the directory *NDBIExample/data* should exactly match what your task would see in */mnt/work/input/*.

To test the Docker container, we need to run our container with the data mounted. **This is different that adding the data using the ADD command in the Dockerfile.** Every time you (or the platform) runs a Docker container, it uses your Dockerfile recipe to remake it. When the container is closed, everything in it goes away! (Remember, this is precisely why we were so careful about creating output locations in our script.) Luckily, running the container with local data temporarily mounted is a lot like the process the platform goes through when using s3 data as task inputs. Here's how we will mount our data, again mimicing what the platform does:

```
docker run -v ~/Full/Path/to/NDBIExample/data:/mnt/work/input -it yourDockerUsername/examplendbi bash
```
Once you're in your container, check the files in */mnt/work/input/*. You should see *ports.json* and a directory called *image* containing the two TIFs.

Now you're ready to test. If you move back to the root and then into *built_up*, you will find the script *justNDBI.py*. You can test by running the script with `python justNDBI.py` here.

Once it runs, check the output. It should be in *mnt/work/output/output* as specified in the script. There will be a TIF file with the suffix *_NDBI.TIF*. If you move back up two levels to *mnt/work/*, you should see a statusfile with your message!

If your script doesn't work correctly the first time, there are a few things to keep in mind:
* Each time you modify your script, you will need to place it in the same local directory as your Dockerfile and rebuild your container. It won't take as long to build as the first time.
* Your data will no longer be mounted when you reopen your container. Be sure to run with the `-v` option described above.

##Step Six: Pushing
Once you're done testing your container locally, push it to DockerHub. To do this:

1. Log in to DockerHub in the terminal window running docker by typing:
  
  ``` docker login --username yourDockerUsername --password y0urP@ssworD ```

2. Make sure you are in the directory containing your Dockerfile. Then type:
  
  ``` docker push yourDockerUsername/examplendbi```

3. Go back to [DockerHub] (https://hub.docker.com). If you click on *Tags* in your *examplendbi* repository, you should now see one called *Latest* that was just updated.

At this point, if you need to make changes to your script or Dockerfile, you will need to rebuild and then repush to DockerHub.

###Congratulations, you've made a docker container that is ready to be registered as a task on the platform.
