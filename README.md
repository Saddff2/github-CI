  # Build, Test, and Push Multi-Arch Docker Images with GitHub Actions
<img width="1513" alt="Screenshot" src="https://github.com/Saddff2/github-CI/assets/133538823/72d08777-8ce8-4ac9-a3dd-82cdef6c0a23">

In today's fast-paced development environment, automating your build, test, and deployment processes is crucial for ensuring efficient and reliable software delivery.

In this guide, We'll walk you through the process of setting up a continuous integration (CI) pipeline using GitHub Actions to build, test, and push a multi-architecture Docker image to DockerHub. Whether you're new to CI/CD pipelines or looking to enhance your existing workflow, this guide will provide the insights and steps you need to get started.

## Why Multi-Arch Docker Images?

Multi-architecture Docker images are a powerful way to ensure your applications can run smoothly across a wider range of hardware platforms. This means building images that are compatible with both AMD64 (the most common architecture) and ARM64 (growing in popularity for mobile and serverless deployments). By creating multi-arch images, you can:

- **Increase Compatibility**: Deploy your application to a broader range of environments without needing to create separate images for each architecture.
- **Simplify Deployment**: Streamline the deployment process by avoiding the need to manage different images for various platforms.
- **Expand User Reach**: Make your applications accessible to a wider user base, including those using ARM-based devices.

## Alternative Container Registries

While **Docker Hub** is a popular choice for storing Docker images, there are other options available, including:

- **Amazon ECR (Elastic Container Registry)**: AWS-managed container registry.
- **Google Container Registry**: Google Cloud-managed container registry.
- **Azure Container Registry**: Microsoft Azure-managed container registry.

### Contents
- [Step 1: Python App](#step-1-python-app)
- [Step 1.1: NodeJS App [**OPTIONAL**]](#step-11-nodejs-app-optional)
- [Step 2: Dockerfile](#step-2-dockerfile)
- [Step 2.0.1: NodeJS Dockerfile [**OPTIONAL]**](#step-201-nodejs-dockerfile-optional)
  - [Step 2.1: Dockerfile explanation](#step-21-dockerfile-explanation)
  - [Step 2.2: Test the Container Locally](#step-22-test-the-container-locally)
  - [Step 2.2.1: Test the NodeJS container locally [**OPTIONAL**]](#step-221-test-the-nodejs-container-locally-optional)
- [Step 3: Create Dockerhub Account and Repository](#step-3-create-dockerhub-account-and-repository)
- [Step 4: Github Actions Workflow](#step-4-github-actions-workflow)
  - [Step 4.1: Writing CI Pipeline](#step-41-writing-ci-pipeline)
  - [Step 4.2: Declaring variables in Repository secrets](#step-42-declaring-variables-in-repository-secrets)
  - [Step 4.3: Explaining the workflow code](#step-43-explaining-the-workflow-code)
  - [NodeJS Workflow Code [**OPTIONAL**]](#nodejs-workflow-code-optional)
  - [Full Workflow Code](#full-workflow-code)
    - [Section 1 - name, triggers, env](#section-1---name-triggers-env)
    - [Section 2 - running jobs](#section-2---running-jobs)
    - [Section 3 - Building and Testing](#section-3---building-and-testing)
    - [Section 4 - Building and Pushing final Image](section-4---building-and-pushing-final-image)
- [Conclusion](#conclusion)
- [Final Result](#final-result)
- [Additional Resources](#additional-resources)
- [Next Steps](#next-steps)
- [Feedback](#feedback)
- [Thank You](#thank-you)
  
## So, What we need?

- **Python App** (**NodeJS** version is also provided, but you can rewrite Dockerfile for your specific app and this pipeline will work)
- **Dockerfile**
- **Dockerhub account** (or any other container registry)
- **Github Actions Workflow**

## Let's break down the steps.

### Step 1: Python App

For this example, I will use a simple Flask application written in Python.

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Daniel Tsoref"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

This is a simple web app that will be running on Flask default port 5000. 

### Step 1.1 NodeJS App [Optional]

<details>
    <summary><b>NodeJS App Variant</b></summary>
  
```
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello from Daniel Tsoref');
});

app.listen(3000, () => {
    console.log('Server listening on port 3000');
});

```

</details>

### Step 2: Dockerfile
```
FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]

```
### Step 2.0.1: NodeJS Dockerfile [OPTIONAL]
<details><summary><b>NodeJS Dockerfile Variant</b></summary>
  
```
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

</details>


### Step 2.1: Dockerfile explanation
<details><summary><b>CLICK HERE.</b></summary>

* **FROM python:3.12.1-alpine3.19**

I'll be using the official Python image based on Alpine linux.
**Alpine Linux** is a lightweight distribution that is perfect for containers.

* **WORKDIR /app**

This will set the working directory to **/app** in the container. All shell commands will run there.

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

This instruction specifies the default command to run when the container starts.

>[!NOTE]
>**CMD** instruction can only be used once in Dockerfile, if you want to run other scripts while container is creating, use the **RUN** instruction.

* **EXPOSE 5000**

Expose the port that the container runs on.

</details>

### Step 2.2: Test the container locally.

Run Docker commands in folder to create an image.
```
docker build -t flask-container:0.1 .
docker run -p 5000:5000 flask-container:0.1
```
If port 5000 is unavailable, you can change the local port, for example:

```docker run -p 5001:5000 flask-container:0.1``` 

It will bind your local port 5001 to the container's port 5000.


<img width="938" alt="Screenshot" src="https://github.com/Saddff2/github-CI/assets/133538823/655a2526-82f6-4d39-b1fb-e9b80cff8995">

### Step 2.2.1: Test the NodeJS container locally [OPTIONAL]

<details><summary><b>Testing the Container</b></summary>
  
```
docker build -t node-container:0.1 .
docker run -p 3000:3000 node-container:0.1
```

<img width="902" alt="Screenshot 2024-05-29 at 12 31 05" src="https://github.com/Saddff2/github-CI/assets/133538823/30edd1d2-63b5-4069-9ced-b8712b861c4d">

</details>

## **Step 3: Create Dockerhub Account and Repository**

* Go to [hub.docker.com](https://hub.docker.com/signup), you can choose **Create account** or **Continue with Github**.

* **Create a new repository** (public or private, it doesn't matter)

>[!NOTE]
>You need to name the repository the same way as your Docker image.

**Step-by-step**
<details><summary><b>Click</b></summary>
  
1. Signing in
   
<img width="473" alt="Screenshot 2024-05-29 at 12 43 10" src="https://github.com/Saddff2/github-CI/assets/133538823/f78ea199-9a7f-4e89-bf47-8874e5ed6564">
<img width="418" alt="Screenshot 2024-05-29 at 12 39 52" src="https://github.com/Saddff2/github-CI/assets/133538823/4579e575-4b7c-48c8-ae18-ed10090bdbc3">


2. Creating repository
  
<img width="908" alt="Screenshot 2024-05-29 at 12 40 14" src="https://github.com/Saddff2/github-CI/assets/133538823/935a4de3-08a5-45d6-88ea-3833199d7d8e">
<img width="742" alt="Screenshot 2024-05-29 at 12 40 31" src="https://github.com/Saddff2/github-CI/assets/133538823/5ed4fc39-42eb-43cd-970b-c5b0304f8a26">


3. Repository created
  
<img width="1173" alt="Screenshot 2024-05-29 at 12 40 43" src="https://github.com/Saddff2/github-CI/assets/133538823/3062f797-69c8-40ed-8af5-e09b35301475">

</details>


## **Step 4: Github Actions Workflow**
**Creating CI Pipeline in GitHub Actions**

For the workflow to work, we need to create a directory `.github/workflows` in your GitHub repository and create a YAML file.

Let's create it.

<img width="640" alt="Screenshot" src="https://github.com/Saddff2/github-CI/assets/133538823/6995a000-5ac9-4f10-b9e6-0e2249c74475">

### **Step 4.1: Writing CI Pipeline**
First, let's talk about **Docker**. 

**Docker** is using your current hardware for building it's containers. So if you're working on **ARM/64**
and want to run Docker images on **AMD/64** architecture, you need to specify platform that **Docker** image 
is created for. 

In this **CI Pipeline** we will be using Github Action's ubuntu-latest image that is on **AMD/64** architecture
like most of **Linux** servers are. 

So we need to install **QEMU** - open-source hardware virtualization and emulation tool that will allow us to build also for **ARM/64**.

>[!NOTE]
>This is just an option for images. If you don't need **ARM/64** architecture, feel free not to install **QEMU** and not build for **ARM/64**.
>Howerver, it's nice to have multi-platform image.

### Step 4.2: Declaring variables in Repository secrets.
- Go to Repository **Settings**
- On the left side click **Secrets and variables** -> **Actions**
- Click **New repository secret**

**In this workflow, you'll need to define 2 repository secrets**

1. **DOCKER_USERNAME**  _for **value**, write down your Docker Hub **Username**_
2. **DOCKER_ACCESS_TOKEN** _for **value**, create a Docker Hub Access Token at **hub.docker.com**->**My Account**->**Security**->**New Access Token**_

<img width="808" alt="Screenshot 2024-05-29 at 12 07 58" src="https://github.com/Saddff2/github-CI/assets/133538823/136a4762-2b34-4165-b9d5-d36ea1486672">
 
I will be using 3 environment variables named **IMAGE_NAME**, **DOCKER_REGISTRY** and **APP_PORT**, which are declared directly in the workflow file.

If you need to use a **different registry**, check out [docker/login-action documentation](https://github.com/docker/login-action)


### Step 4.3: Explaining the workflow code.

### NodeJS Workflow Code [OPTIONAL]

<details><summary><b>NodeJS Workflow</b></summary>

It's very easy as the **only** thing we need to change is **APP_PORT** in env variables.
In Python we are using port 5000, and in NodeJS the port is 3000.

```
on:
  push:
    branches:
      - main
env: 
  IMAGE_NAME: web-app
  DOCKER_REGISTRY: docker.io
  APP_PORT: 3000

```

**Full Code**

```
name: Build Test and Push Mutli Platform Docker Image

on:
  push:
    branches:
      - main

env: 
  IMAGE_NAME: web-app
  DOCKER_REGISTRY: docker.io
  APP_PORT: 3000

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
      
    - name: Setup QEMU
      uses: docker/setup-qemu-action@v3
      
    - name: Setup Dockerx build
      uses: docker/setup-buildx-action@f95db51fddba0c2d1ec667646a06c2ce06100226

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with: 
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_ACCESS_TOKEN }}

    - name: Determine version number
      id: determine_version
      run: |
        BUILD_DATE=$(date +%d-%m-%Y)
        echo "BUILD_DATE=$BUILD_DATE" >> $GITHUB_ENV
        BUILD_NUMBER=$(git rev-parse --short HEAD)
        echo "BUILD_NUMBER=$BUILD_NUMBER" >> $GITHUB_ENV

    - name: Build AMD/64 Platform Container 
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64
        push: false
        load: true
        tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}

    - name: Run Container
      run: |
        docker run -d -p ${{ env.APP_PORT}}:${{ env.APP_PORT}} \
        -e BUILD_DATE=${{ env.BUILD_DATE }} \
        --name web-app-test \
        ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}

    - name: Wait for Container to be Ready
      run: |
        echo "Waiting for container to be ready..."
        sleep 10

    - name: Test Web App
      id: test_app
      run:
        curl -sSf http://localhost:${{ env.APP_PORT}} || exit 1

    - name: Push Multi Platform Image
      uses: docker/build-push-action@v5 
      if: success() && steps.test_app.outcome == 'success'
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Logout from Docker
      run: docker logout
```

</details>


### Full Workflow Code
<details>
    <summary><b>WORKFLOW</b></summary>

```
name: Build Test and Push Mutli Platform Docker Image
on:
  push:
    branches:
      - main
      
env: 
  IMAGE_NAME: web-app
  DOCKER_REGISTRY: docker.io
  APP_PORT: 5000
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    
    - name: Checkout Repository
      uses: actions/checkout@v4
      
    - name: Setup QEMU
      uses: docker/setup-qemu-action@v3
      
    - name: Setup Dockerx build
      uses: docker/setup-buildx-action@f95db51fddba0c2d1ec667646a06c2ce06100226
      
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with: 
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_ACCESS_TOKEN }}
        
    - name: Determine version number
      id: determine_version
      run: |
        BUILD_DATE=$(date +%d-%m-%Y)
        echo "BUILD_DATE=$BUILD_DATE" >> $GITHUB_ENV
        BUILD_NUMBER=$(git rev-parse --short HEAD)
        echo "BUILD_NUMBER=$BUILD_NUMBER" >> $GITHUB_ENV
        
    - name: Build AMD/64 Platform Container 
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64
        push: false
        load: true
        tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Run Container
      run: |
        docker run -d -p ${{ env.APP_PORT }}:${{ env.APP_PORT }} \
        --name web-app-test \
        ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Wait for Container to be Ready
      run: |
        echo "Waiting for container to be ready..."
        sleep 5
        
    - name: Test Web App
      id: test_app
      run:
        curl -sSf http://localhost:${{ env.APP_PORT }} || exit 1
        
    - name: Push Multi Platform Image
      uses: docker/build-push-action@v5 
      if: success() && steps.test_app.outcome == 'success'
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Logout from Docker
      run: docker logout

      
  ```
    
</details>


### **Section 1 - name, triggers, env.**
```
name: Build Test and Push Mutli Platform Docker Image
on:
  push:
    branches:
      - main
env: 
  IMAGE_NAME: web-app
  DOCKER_REGISTRY: docker.io
  APP_PORT: 5000
jobs:
  build:
  
```

- **name** - name of the pipeline, can be any that you want.

- **on, push, branches** - actions that **trigger** the pipeline, in our case it will be triggered when someone **pushes** commit to **main** branch.

For example, you can write more branches or use `on: pull_request: branches: -main` - that will trigger the pipeline when a pull request is created.

There's a lot more specific triggers; check out [**official documentation**](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

- **env** - environment variables that will be available for this specific workflow, you can also create such variables in the **jobs** and **steps**.

- **IMAGE_NAME** - name of your image.

- **DOCKER_REGISTRY** - In our case it's Docker Hub, but you can specify other container registry and use it in your workflow, check out [docker/login-action documentation](https://github.com/docker/login-action) to correctly implement it.
  
- **APP_PORT** - port of our application, for NodeJS version of the guide, it will be 3000.

### **Section 2 - running jobs.**

```
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
    - name: Setup QEMU
      uses: docker/setup-qemu-action@v3
    - name: Setup Dockerx build
      uses: docker/setup-buildx-action@f95db51fddba0c2d1ec667646a06c2ce06100226
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with: 
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_ACCESS_TOKEN }}

```


- **jobs** - There can be more jobs if you want that will be running in workflow.

- **build** - Name of the job.

- **runs-on** - There's a list of available images that jobs will be run on. For example, you can use **macos** or **windows** as image.

- **steps** - Each step needs to have a name and a script specifying what it will do.

- **uses** - GH Actions provide us scripts that we can use for regular things.



### **Section 3 - Building and Testing.**


```
 - name: Determine version number
      id: determine_version
      run: |
        BUILD_DATE=$(date +%d-%m-%Y)
        echo "BUILD_DATE=$BUILD_DATE" >> $GITHUB_ENV
        BUILD_NUMBER=$(git rev-parse --short HEAD)
        echo "BUILD_NUMBER=$BUILD_NUMBER" >> $GITHUB_ENV
        
    - name: Build AMD/64 Platform Container 
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64
        push: false
        load: true
        tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Run Container
      run: |
        docker run -d -p ${{ env.APP_PORT}}:${{ env.APP_PORT}} \
        --name web-app-test \
        ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Wait for Container to be Ready
      run: |
        echo "Waiting for container to be ready..."
        sleep 5
        
    - name: Test Web App
      id: test_app
      run:
        curl -sSf http://localhost:${{ env.APP_PORT}} || exit 1
```

- **Determine version number** - Use the current date and commit hash to determine the version for the image tag.

- **Build AMD/64 Platform Container** - Build the image for test purposes on only one platform to save time.

>[!IMPORTANT]
>Use **load:true** to make image available to use locally after build.

- **Run container** - Run the recently created image.

- **Waiting for container to start** - This step is not always needed.

- **Test Web App** - Test the app using a simple bash command. If the command does not succeed, it exits from workflow.
  
>[!Note]
>**You can change this step to Unit tests.**



### **Section 4 - Building and Pushing final Image.**

```
    - name: Push Multi Platform Image
      uses: docker/build-push-action@v5 
      if: success() && steps.test_app.outcome == 'success'
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:${{ env.BUILD_DATE }}.${{ env.BUILD_NUMBER }}
        
    - name: Logout from Docker
      run: docker logout

```

- **Build and Push final Multi Platform Image** - Use **if** to determine if previous steps and **Test Web App** was successed based on it's ID. 

- **platforms** - Build for multiple architectures using QEMU installed previously.

- **push** - Push to Container Repository.

- **tags** - needs to contain repository_name/your_image_name:tags

- **Logout** - ensures that any authentication credentials used to access the Docker registry are cleared from the runner's environment.

## Conclusion

By following these steps, you can successfully automate the build, test, and push process for multi-arch Docker images using GitHub Actions. This streamlined approach will significantly enhance your CI/CD pipeline, leading to faster development cycles, increased code quality, and broader application reach.

## Final Result

**Here's what our final result might look like:**

### **Workflow Run**
  
<img width="1624" alt="Screenshot 2024-05-29 at 12 14 57" src="https://github.com/Saddff2/github-CI/assets/133538823/d14bc29a-19b5-4e02-9d6a-70a489631798">

### **Multi-Arch Image on Docker Hub**


<img width="677" alt="Screenshot 2024-05-29 at 12 10 36" src="https://github.com/Saddff2/github-CI/assets/133538823/db90634b-5d70-4eab-a30a-ac9f621d3677">


## Next Steps

Now that you have a working CI/CD pipeline, here are a few additional steps you might consider:
1. **Enhance Testing**: Expand your testing suite to include more comprehensive unit and integration tests.
2. **Deployment**: Integrate deployment steps into your workflow to automatically deploy your application to cloud services like AWS, Azure, or Google Cloud.
3. **Notifications**: Set up notifications or alerts to keep your team informed about the status of your builds.
4. **Pipeline Optimization**: Refactor and optimize your pipeline for faster build times and better resource usage.

## Additional Resources	
Explore more advanced features and best practices:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Buildx Documentation](https://github.com/docker/buildx)


## Feedback
Your **feedback** is **valuable**! If you encountered any **issues** or have **suggestions** for improvement, please **feel free** to open an issue or pull request on the [GitHub repository](https://github.com/Saddff2/github-CI). Your contributions help make this guide better for everyone.

## Thank You
Thank you for following along with this guide! I hope this has been helpful in automating your development process with GitHub Actions. 



