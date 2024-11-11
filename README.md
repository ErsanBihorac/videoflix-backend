# Videoflix (backend)

**Description**: This is the backend of my video streaming web application "Videoflix".

## Table of Contents

1. [About the Project](#about-the-project)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Documentation](#api-documentation)
7. [Testing](#testing)
8. [License](#license)

## About the Project

- This project is a RESTful API backend for a video streaming application
- It allows users to register, verify the account, login, reset the password, request a new password
- Besides that you can upload your own videos with thumbnails, the backend handles the formatting of the thumbnail and the videos
- The videos will afterwards be available in 3 different qualities to stream from (1080p, 720p, 480p) and there will be a video preview when the video is selected on the dashboard

## Technologies

- **Python** 3.12
- **Django** 5.1.1
- **Django REST framework** for building the API
- **RQ win** for running complex tasks in the background
- **PostgreSQL** for database management

## Prerequisites

List any software or dependencies that are required to run this project.

- Python 3.12 or higher
- A virtual environment manager like `venv`
- PostgreSQL or another compatible database

## Installation

Step-by-step instructions for setting up the project locally.

1. **Clone the repository**

    ```bash
    git clone https://github.com/ErsanBihorac/videoflix-backend.git
    cd videoflix-backend

2. **Create a virtual environment**

    ```bash
    python3 -m venv env
    source env/bin/activate

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt

4. **Configure the database**

    Ensure PostgreSQL is running, and set the databse credentials in videoflix-backend/videoflix settings.py

5. **Run database migrations**

    ```bash
    python manage.py migrate

6. **Create .env with credentials**

    ```bash
    touch .env
    nano .env
    
7. **paste credentials with your own values(important) and save the file**

    ```bash
    "EMAIL_HOST_USER=your email address to send emails
    EMAIL_HOST_PASSWORD=the password to let third parties use your email
    POSTGRESQL_PASSWORD=your postgresql server password
    POSTGRESQL_HOST=localhost"
    

8. **Create a superuser (optional)**

    ```bash
    python manage.py createsuperuser
    follow the instructions of the console

9. **Start the server**

    ```bash
    python manage.py runserver

## Usage

- First of all you need to upload videos in your backend, you need a thumbnail (image in jpg format) and a video (video in mp4 format)
- Visit the admin panel `http://localhost:8000/admin` and log in with your superuser credentials
- Go to the `Content` section and then to `Videos`, give your video a title, description, upload the thumbnail, video and give it a category
- Save your video, the backend will handle the process of converting the video automatically by itself

- After creating a video for your application you can register a new account, verfify it in the email that will be sent, log in to Videoflix and enjoy watching your video!

## API Documentation

This section outlines the main endpoints provided by the API, along with example requests and responses.

**Authentification Endpoints**

- POST `/api/login/`
Logs a user into the system.

- POST `/api/register/`
Registers a user in the system.

- GET `/api/email-verify/`
Verifies the account after registering.

- POST `/api/request-reset-email/`
Sends an e-mail to reset the password.

- GET `/api/password-reset/<uidb64>/<token>/`
Checks if the password token is valid.

- PATCH `/api/password-reset-complete/`
Replaces the old password.

- POST `/api/check-registered-email/`
Checks if the e-mail is registered.

**API CONTENT Endpoints**

Content endpoints provide functionality for managing the video progress of viewed videos and receiving the list of available videos. The following endpoints are available: 

- GET `/api/content/videos/`
Returns a list of all available videos.

- GET `/api/content/video-progress/in_progress`
Returns a list of all videos that have a progress of being viewed.

- POST `/api/content/video-progress/<video_id>/save_progress`
Saves the progress of a video that has ben viewed.

## Testing

Instructions for running the automated tests for the project.

1. **Run tests**

Execute all tests:

    python manage.py test

2. **Check test coverage**

get test coverage of the whole application:

    coverage run --source='.' manage.py test
    coverage report -m

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software in accordance with the terms of the MIT License. See the [LICENSE](LICENSE) file for full details.