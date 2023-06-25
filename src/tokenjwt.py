from datetime import datetime, timedelta
from conections import RedisConnection
from config import env_config
import jwt


class TokenStorage:
    secret_key = env_config.secret_key
    token_expire_minutes = 10
    _connection = RedisConnection.get_connection()

    @staticmethod
    def generate_token(email: str) -> str:
        """
        Generate a JWT token for the given email address.
        :param email: Email address to generate the token for
        :return: Generated JWT token
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=TokenStorage.token_expire_minutes),
            "iat": datetime.utcnow(),
            "sub": "login",
            "email": email
        }
        token = jwt.encode(payload, TokenStorage.secret_key, algorithm="HS256")
        return token

    @staticmethod
    def store_token(email: str, token: str) -> None:
        """
        Store the token in Redis for the given email address.
        :param email: Email address to store the token for
        :param token: JWT token to be stored
        """
        RedisConnection.set_value(email, token)

    @staticmethod
    def token_to_email(token: str) -> str:
        """
        Extract the email address from the JWT token.
        :param token: JWT token
        :return: Extracted email address
        """
        payload = jwt.decode(token, TokenStorage.secret_key, algorithms=["HS256"])
        decoded_email = payload.get("email")
        return decoded_email

    @staticmethod
    def validate_token(token: str) -> bool:
        """
        Validate the JWT token.
        :param token: JWT token to be validated
        :return: True if the token is valid, False otherwise
        """
        email = TokenStorage.token_to_email(token)
        stored_token = RedisConnection.get_value(email)
        if stored_token is None or stored_token.decode() != token:
            return False
        try:
            payload = jwt.decode(token, TokenStorage.secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            RedisConnection.del_value(email)
            return False
        except jwt.InvalidTokenError:
            return False


if __name__ == '__main__':
    t = TokenStorage()
    # token = t.generate_token("reza@gmail.com")
    # t.store_token("reza@gmail.com", token)
    # print(t.token_to_email(token))
    # RedisConnection.get_value("reza@gmail.com")
    # print(str(token))
