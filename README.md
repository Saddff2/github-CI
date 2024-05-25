# GitHub Actions Docker Image Build Test and Push to Dockerhub

Recently I've been working with GitHub Actions on my project and I wanted to share knowledge that I've earned.

## So, What we need?

- **Python App** (or any app that you want)
- **Dockerfile**
- **Github Workflow**
- **Dockerhub account** (or any other container registry)

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
Alpine Linux is low weight distribution that is perfect for containers
But main difficulty with it is that you need to install all the packages 
and app dependecies.












