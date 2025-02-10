# Embedded Lab Manager WebApp

Embedded Lab Manager is a web-based application for managing lab resources and activities. This repository contains the source code, along with detailed instructions for setting up the development environment and deploying the project.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Repository Links](#repository-links)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is built with Python and Django. It uses a virtual environment to manage dependencies for development and Docker for production deployments. For containerized deployment instructions, please see the [DOCKER.md](DOCKER.md) file.

## Getting Started

### Prerequisites

Ensure you have **Python 3.x** installed:

- **Linux (Ubuntu/Debian):**
  
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip -y
  python3 --version
  pip3 --version```

- **Windows/macOS:**
  
  Download the latest stable release from the official Python website. During installation, make sure to select "Add Python to PATH". Verify installation by running:

  ```bash
  python --version 
  pip --version
  ```

### CLoning the Repository

Clone the repository either SSH or HTTPS.

- **Using SSH**

  `git clone git@github.com:urasayanoglu/emblab-manager-webapp.git`

  or alternatively:

  `git clone git@git.dc.turkuamk.fi:embo/emblab-manager-webapp.git`

- **Using HTTPS**

  `git clone https://github.com/urasayanoglu/emblab-manager-webapp.git`

  or:

  `git clone https://git.dc.turkuamk.fi/embo/emblab-manager-webapp.git`

### Setting Up the Development Environment

1. **Create a Virtual Environment**

  Creating a virtual environment isolates your project’s dependencies from your system-wide Python installations.

- **Linux/macOS**

  ```bash
  python3 -m venv emblab_env
  source emblab_env/bin/activate
  ```

- **Windows**

  ```powershell
  python -m venv emblab_env
  .\emblab_env\Scripts\activate
  ```

2. **Install Dependencies**

  Once the virtual environment is activated, install the required packages from the `requirements.txt` file:

  `pip install -r requirements.txt`

  Key dependencies include Django, Pillow (for image processing), and Gunicorn (for production deployment).

3. **Initialize the Project**

- **Create a Superuser**
  `python manage.py createsuperuser`

  Follow the prompts to provide a username, email (optional), and password.

- **Apply Database Migrations**

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## Running the Application

Start the Django development server:
`python manage.py runserver`

Once running, access the application in your web browser at http://localhost:8000. 

After running the development server, the Embedded Lab Manager project starts with no inventory items, bookable tables, resources, or background images pre-registered. To fully configure the system, users need to log into the admin panel using the username and password created during the setup process. To manage the application via the admin panel, navigate to http://localhost:8000/admin/.

## Deployment

For containerized deployments, refer to the separate Docker deployment instructions in DOCKER.md. This guide explains how to install Docker, build images, and manage containers for the Embedded Lab Manager.

## Repository Links

- GitHub:  https://github.com/urasayanoglu/emblab-manager-webapp
- GitLab:  https://git.dc.turkuamk.fi/embo/emblab-manager-webapp

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests. If you plan on making significant changes, consider opening an issue first to discuss your ideas.

## License

This project is licensed under the GNU General Public License V3.0 . See the [LICENSE](./LICENSE) file for more information.