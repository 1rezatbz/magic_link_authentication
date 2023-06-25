# Magic Link Authentication

![Project Logo](path/to/logo.png)

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

## Installation

1. Clone the repository:
2. Install the required dependencies:
3. Configure the environment variables in the `.env` file:
4. Access the API at `http://localhost:8000`

## Usage

1. Register a new user by sending a POST request to `/register` endpoint with the following JSON payload:
2
```json
{
  "email": "user@example.com"
}





