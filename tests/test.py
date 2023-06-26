import unittest
from starlette.testclient import TestClient
from src.conections import RedisConnection
from src.schemas import UserRegistration, User
from src.crud import create_users_table
from apis import app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        create_users_table()

    # def tearDown(self):
    #     if os.path.exists(env_config.sqlite_file):
    #         os.remove(env_config.sqlite_file)
    #         print("Test db deleted successfully.")
    #     else:
    #         print("Test db does not exist.")

    def test_register_user_success(self):
        # Test case for successful user registration
        email = "test@example.com"
        user = UserRegistration(email=email)

        response = self.client.post("/register", json=user.dict())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Registration successful"})

    def test_register_user_invalid_email_format(self):
        # Test case for invalid email format during user registration
        email = "invalidemail"
        user = UserRegistration(email=email)

        response = self.client.post("/register", json=user.dict())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid email address format"})

    def test_register_user_already_registered(self):
        # Test case for already registered email during user registration
        email = "test@example.com"
        user = UserRegistration(email=email)

        response = self.client.post("/register", json=user.dict())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Email already registered"})

    def test_send_magic_link_success(self):
        # Test case for successful sending of magic link
        email = "test@example.com"
        magic_link = User(email=email)

        response = self.client.post("/login", json=magic_link.dict())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Magic link sent"})

    def test_send_magic_link_invalid_email_format(self):
        # Test case for invalid email format during sending of magic link
        email = "invalidemail"
        magic_link = User(email=email)

        response = self.client.post("/login", json=magic_link.dict())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid email address format"})

    def test_send_magic_link_unregistered_email(self):
        # Test case for sending magic link to an unregistered email
        email = "unregistered@example.com"
        magic_link = User(email=email)

        response = self.client.post("/login", json=magic_link.dict())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Email address is not registered"})

    def test_login_success(self):
        # for executing this test , insure toke is in redis
        token = RedisConnection.get_value("test@example.com").decode()
        response = self.client.get(f"/login/token={token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Login successful"})

    def test_login_invalid_or_expired_token(self):
        # for executing this test , insure toke is in redis, and it is expired
        token = RedisConnection.get_value("test@example.com").decode()
        response = self.client.get(f"/login/token={token}")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid or expired token"})


if __name__ == '__main__':
    unittest.main()
