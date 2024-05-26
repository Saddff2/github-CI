# GitHub Actions Multi-Architecture Docker Image Build Test and Push to Dockerhub

Recently I've been working with GitHub Actions on my project and I wanted to share knowledge that I've gained.

## So, What we need?

- **Python App** (or any app that you want)
- **Dockerfile**
- **Dockerhub account** (or any other container registry)
- **Github Actins Workflow**

## Let's break down the steps.

### Python App

For app example I'll be using simple Flask application written in python.

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Daniel Tsoref"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```

This is simple web app that will be running on Flask default port 5000. 

### Dockerfile
```
FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "app.py"]

EXPOSE 5000
```
* **FROM python:3.12.1-alpine3.19**

I'll be using official Python image based on Alpine linux.
**Alpine Linux** is low-weight distribution that is perfect for containers.

* **WORKDIR /app**

This will set working directory to /app in the container. All the shell commands will run there.

* **COPY requirements.txt /app/requirements.txt**

Copy the requirements file into the container. 
>[!IMPORTANT]
>You need to create **requirements.txt** file **prior** using ```pip freeze > requirements.txt``` in the app's folder.

* **RUN pip install --no-cache-dir -r requirements.txt**

Install any dependencies specified in requirements.txt.

**Note** that we install all requirements before copying all the app into container.
This will optimize container layers and potentially decrease time building.

* **COPY . /app**

Copy the rest of the application code into the container

* **CMD ["python", "app.py"]**

This instruction runs the default command to run when the container starts.

>[!NOTE]
>**CMD** instruction can only be used once in Dockerfile, if you want to run other scripts while container is creating use **RUN** instruction.

* **EXPOSE 5000**

Expose the port that container runs on.

## Now, let's test the container locally.

Run docker commands in folder to create an image.
```
docker build -t flask-container:0.1 .
docker run -p 5000:5000 flask-container:0.1
```
If port 5000 is unavailable, you can change the local port, for example:

```docker run -p 5001:5000 flask-container:0.1``` 

It will bound your 5001 port to 5000 container's port.

<img width="944" alt="Screenshot 2024-05-26 at 16 42 12" src="https://github.com/Saddff2/github-CI/assets/133538823/6250a037-c500-4279-96ac-5621b1b4fcd2">



## **Create Dockerhub Account and Repository**

* Go to [hub.docker.com(https://hub.docker.com/signup), you can choose **Create account** or **Continue with Github**.

* **Create a new repository** (public or private, it doesn't matter)

>[!NOTE]
>You need to name the repository the same way as your docker image.

## **Github Actions Workflow**
**Creating CI Pipeline in GitHub Actions**

First things first you need to create a directory .github/workflows in your github repository and make a yml file. 

Let's create it.

<img width="640" alt="Screenshot 2024-05-26 at 13 51 41" src="https://github.com/Saddff2/github-CI/assets/133538823/6995a000-5ac9-4f10-b9e6-0e2249c74475">

### Writing CI Pipeline
First, let's talk about **Docker**. 

**Docker** is using your current hardware for building it's containers. So if you're working on **ARM/64**
and want to run Docker images on **AMD/64** architecture you need to specify platform that **Docker** image 
is created for. 

In this **CI Pipeline** we will be using Github Action's ubuntu-latest image that is on **AMD/64** architecture
like most of **Linux** servers are. 

So we need to install **QEMU** - open-source hardware virtualization and emulation tool that will allow us to build also for **ARM/64**.

>[!NOTE]
>This is just an option for images. If you don't need **ARM/64** architecture, feel free not to install **QEMU** and not building for **ARM/64**.
>But it's nice thing to have multi-platform image.

## Let's declare variables in Repository secrets.
- Go to Repository **Settings**
- On the left side click **Secrets and variables** -> **Actions**
- Click **New repository secret**

**In this workflow you'll need to define 2 Repository secrets**

1. **DOCKER_USERNAME**  _for **value** write down your DOCKERHUB **Username**_
2. **DOCKER_ACCESS_TOKEN** _for **value** create in DOCKERHUB Access Token **hub.docker.com**->**My Account**->**Security**->**New Access Token**_
 
And I'll be using 2 enviroment variables named **IMAGE_NAME** and **DOCKER_REGISTRY** that is declared directly in workflow file.

If you need to use different registry, check out [docker/login-action documentation](https://github.com/docker/login-action)






