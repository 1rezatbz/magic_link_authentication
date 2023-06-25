import sqlite3
import requests
from config import env_config
from conections import SqlLiteConnection


def create_users_table():
    """
    Create the users table in the database if it doesn't exist.
    """
    conn = SqlLiteConnection()
    query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE)"
    conn.execute(query)
    conn.disconnect()


def is_valid_email(email: str) -> bool:
    """
    Check if the provided email address is valid using the Mailboxlayer API.
    :param email: Email address to validate
    :return: True if the email is valid, False otherwise
    """
    api_key = env_config.mailboxlayerApiKey
    url = f"http://apilayer.net/api/check?access_key={api_key}&email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        return result.get("format_valid") and result.get("mx_found")
    return False


def register_user(email: str):
    """
    Register a new user in the database.
    :param email: Email address of the user to register
    """
    conn = SqlLiteConnection()
    try:
        # Check if the user already exists
        existing_user = check_user_exists(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Insert the new user into the database
        query = "INSERT INTO users (email) VALUES (?)"
        conn.execute(query, (email,))
        user_id = conn.cursor.lastrowid
        print(f"User registered with ID: {user_id}")
    except sqlite3.Error as e:
        print(f"Error registering user: {e}")
    finally:
        conn.disconnect()


def check_user_exists(email: str) -> bool:
    """
    Check if a user already exists in the database.
    :param email: Email address of the user to check
    :return: True if the user exists, False otherwise
    """
    conn = SqlLiteConnection()
    try:
        query = "SELECT id FROM users WHERE email=?"
        conn.execute(query, (email,))
        existing_user = conn.fetch_one()
        if existing_user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Error checking user existence: {e}")
    finally:
        conn.disconnect()


def send_email(email: str, token: str, subject: str = "Access Link"):
    """
    Send a magic link email to the provided email address.
    :param email: Email address to send the email to
    :param token: Access token for the login link
    :param subject: Subject of the email (default: "Access Link")
    """
    url = "https://api.mailgun.net/v3/sandbox67138bc3cc7745bf80fbe0313d43e397.mailgun.org/messages"
    api_key = env_config.mailgunApiKey
    login_url = f"http://localhost:8000/login/token={token}"
    data = {
        "from": "Mailgun Sandbox <postmaster@sandbox67138bc3cc7745bf80fbe0313d43e397.mailgun.org>",
        "to": "Reza tabriz " + email,
        "subject": subject,
        "text": f"Dear customer, click the following link to log in: {login_url}",
    }
    print(data)
    response = requests.post(url, auth=("api", env_config.mailgunApiKey), data=data)
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email. Status code:", response.status_code)


if __name__ == '__main__':
    is_valid_email("rezartabriz@yahoo.com")
    # register_user("rezartabriz@yahoo.com")
    # check_user_exists("rezartabriz@yahoo.com")
    # create_users_table()
