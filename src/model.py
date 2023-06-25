from pydantic import BaseModel


class User(BaseModel):
    """
    Model representing a magic link request.
    """
    email: str


# Create a token model for request validation
class TokenModel(BaseModel):
    """
    Model representing a token for request validation.
    """
    token: str


# Create a user registration model for request validation
class UserRegistration(BaseModel):
    """
    Model representing a user registration request.
    """
    email: str
