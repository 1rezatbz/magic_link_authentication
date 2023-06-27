# Magic Link Authentication

Magic Link Authentication is a secure and user-friendly authentication system that replaces traditional username-password combinations with magic links. This project provides a modern and hassle-free approach to user authentication, enhancing security while improving the user experience.

## Features

- User registration with email verification
- Generation and sending of magic links via email
- Token-based authentication for login validation
- Secure storage of user data
- Error handling and graceful response messages

## Technologies Used

- Python
- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python
- Pydantic: Data validation and serialization library for Python
- Tokenjwt: Library for generating and validating tokens
- HTTPX: HTTP client for sending emails
- SQLite: Lightweight and serverless database engine for data storage

## Prerequisites

- Python 3.9
- Pipenv

## Installation

1. Clone this repository: `git clone https://github.com/1rezatbz/magic_link_authentication.git`
2. Build python environment(or set you python interpreter) 
3. Install the requirements: `pip install -r requirements.txt`
4. Install Redis database or change the host and the port to the existing redis connection.
5. Mark Src Directory as source root
5. Run project with using run.py script

## API Endpoints

### User Registration

- **Endpoint:** `/register`
- **Method:** POST
- **Description:** Registers a new user and sends a verification email with a magic link.

### User login I
- **Endpoint:** `/login`
- **Method:** POST
- **Description:** Create Token and send login like the user eamil

### User login II

- **Endpoint:** `/login`
- **Method:** GET
- **Description:** Validates the magic link token and logs in the user.
