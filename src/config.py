import os
from pydantic import BaseSettings

# Get the base directory path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setting up development environment variables
dev_env_path = os.path.join(base_dir, "magic_link_authentication/.env.dev")

# Check if the development environment file exists
if os.path.isfile(dev_env_path):
    # Read the lines from the environment file
    with open(dev_env_path, "r") as file:
        lines = file.readlines()

    # Iterate over each line in the environment file
    for line in lines:
        # Extract the key-value pair from the line
        key, value = line.strip().split("=")

        # Set the environment variable
        os.environ[key] = value


class Config(BaseSettings):
    debug: bool = True  # Debug mode flag
    app_title: str = 'magic_link_authentication'  # Application title
    redis_host: str = ""  # Redis server host
    redis_port: int = 0  # Redis server port
    redis_db: int = 0  # Redis database index
    sqlite_file: str = ""  # SQLite database file path
    mailgunApiKey: str = ""  # Mailgun API key
    mailboxlayerApiKey: str = ""  # Mailboxlayer API key


env_config = Config()  # Create an instance of the Config class for environment configuration


