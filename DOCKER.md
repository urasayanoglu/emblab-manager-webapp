# Deployment Using Docker

This guide provides an overview of deploying the Embedded Lab Manager using Docker. It covers essential concepts, explains the roles of the Dockerfile and Compose file, and gives step-by-step instructions for running the application.

## Installing Docker

Before deploying the Embedded Lab Manager, Docker must be installed on your system.

### For Linux (Ubuntu/Debian)

Run the following commands in a terminal:

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

To verify that Docker is installed correctly, run:

`docker --version`

### For Windows and macOS

For Windows and macOS, download and install Docker Desktop from the [Docker website](https://www.docker.com/). Follow the installation instructions provided there.

### Understanding Dockerfile and Compose.yaml

Docker provides two primary mechanisms for containerizing applications: the Dockerfile and the Compose file (compose.yaml). Each serves a different purpose in the deployment process.

#### Dockerfile

The Dockerfile is a script that contains a set of instructions to build a Docker image. It typically defines:

- The base image (e.g., python:3.10-slim in this project)
- Required dependencies
- Environment variables
- Commands to prepare and start the application

In this repository, the Dockerfile sets up a Python environment, installs dependencies, configures the database, and prepares static files for deployment.

#### Compose.yaml

The Compose file is used to define and run multi-container applications. It allows you to specify multiple services—such as the web application and the database—in a single file. This file simplifies container orchestration by managing interconnected services together.

In this project, the compose.yaml file defines:

- **The web application service:** Built using the Dockerfile.
- **The PostgreSQL database service:** Using the official PostgreSQL Docker image.

**Why Use Both?**

- **Dockerfile:** Provides a step-by-step guide to build a single service container, ensuring consistency across different environments.
- **Compose file:** Automates the deployment of multi-container environments, allowing you to manage dependent services (like databases) alongside the web application.

Using both together offers flexibility—allowing for easy testing with standalone containers and full-scale deployment with multiple services.

### Running the Docker Containers

Once Docker is installed and the necessary files ([Dockerfile](./Dockerfile) and [compose.yaml](./compose.yaml)) are set up, follow these steps to start the application:

1. **Navigate to the Project Directory**
Open your terminal (Linux/macOS) or Command Prompt (Windows) and navigate to the directory containing the **Dockerfile** and **compose.yaml** file.

2. **Build and Start the Containers**
Run the following command to build the Docker images and start the containers:

`docker compose up --build`

The --build flag ensures that the image is rebuilt based on the latest changes in the Dockerfile.

3. **Running in Detached Mode**
To run the containers in the background, use:

`docker compose up -d`

4. **Accessing the Application**
Once the containers are running, the application will be accessible at:

http://localhost:8000

5. **Stopping the Containers**
To stop the running containers, use:

`docker compose down`

### Serving Static Files in Production

In a production environment, it is recommended to serve static files separately from the Django application server (Gunicorn), as Django's built-in server is not optimized for static content.

### Why Use a Separate Static File Service?

- Improved Performance: Offloads static file handling to a lightweight server like Nginx.
- Enhanced Scalability: Allows the web server to focus on dynamic content.
- Optimized Caching: Better caching mechanisms for frequently accessed static assets.

### Running the Static File Service

To serve static files, create a separate container (for example, using Nginx) and add it to your compose.yaml file. This additional service will manage static files alongside your main application. Once configured, build and start the containers with:

`docker compose up -d`

Remember to update your compose.yaml file with the necessary configuration for the static file service.
