# Pokemon Proxy

**Description:**

This project implements a reverse proxy service that interacts with the Pokemon stream API. The service forwards requests, applies specific rules, and tracks various metrics using Django and Redis.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [Endpoints](#endpoints)
5. [Testing](#testing)
6. [Contributing](#contributing)
7. [License](#license)

---

## Installation

### Prerequisites

- Python 3.11.9
- Django 5.1
- Redis
- Celery
- RabbitMQ
- Docker
- Ngrok (for exposing your local server to the internet)
- Postman (for testing the API)

### Steps:

1. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv_proxy
    source venv_proxy/bin/activate  # On Windows use `venv_proxy\Scripts\activate`

2. **Install the Required Dependencies:**

    ```bash
    pip install -r requirements.txt

3. **Run Redis Server:**

    Ensure Redis is running on your local machine. If not, you can start it using:
    
    ```bash
    redis-server

4. **Start the Django Development Server:**
    ```bash
    python manage.py runserver
   
5. **Run Celery:**

    Celery is used for handling asynchronous tasks. To run Celery with the `eventlet` pool, follow these steps:

   Ensure that Celery and Eventlet are installed. You can install them using pip:

   ```bash
   pip install celery eventlet
   # and than run celery :
   celery -A reverse_proxy worker --loglevel=info -P eventlet
   
6. **Docker Compose Setup**

    Docker Compose simplifies the management of multi-container Docker applications. This section explains how to set up and run your application using Docker Compose.

    **Docker Compose File**

    Ensure you have a `docker-compose.yml` file in the root of your project directory. Here’s an example configuration for a Django project with Redis and RabbitMQ.
 
    **Run** the following command to build the Docker images and start the containers defined in your docker-compose.yml file:
    
    ```bash
    docker-compose up --build

7. **Expose Your Server Using Ngrok:**

    ```bash
    ngrok http 8000
   
Use the provided HTTPS URL to interact with your local server.

9. **Usage:**

    Configure the Service:

    Update the config.json file to define the rules for processing requests. Example:
    ```json
    {
      "rules": [
        {
          "url": "http://ce08-46-121-110-99.ngrok-free.app",
          "reason": "awesome pokemon",
          "match": [
            "hit_points==35",
            "type_two!=word",
            "special_defense>10",
            "generation<20"
          ]
        }
      ]
    }
10.  **Make Requests:**

    Use Postman or another HTTP client to send requests to destination URL

    Configuration:
    
    config.json: Contains rules for request forwarding. Ensure that the URL is set to the correct Ngrok URL that you want to be the target.
    
    settings.py: Adjust Django settings such as SECURE_SSL_REDIRECT to enforce **HTTPS**. (OPTIONAL)

11. **Endpoints:**

   1. /stream/: Main endpoint that processes incoming requests based on defined rules.
    
    2. /stats/: Internal endpoint that returns metrics like request count, error rate, incoming/outgoing bytes, and average response time.

12. **Testing**

    Run Tests:
    
    ```bash
    python manage.py test

Test in Postman:

Import the provided Postman collection (if available) and test the endpoints using the Ngrok URL.