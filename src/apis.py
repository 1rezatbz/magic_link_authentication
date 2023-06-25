from fastapi import FastAPI, HTTPException
from model import UserRegistration, User
from crud import create_users_table, is_valid_email, register_user, check_user_exists, send_email
from tokenjwt import TokenStorage

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """
    Function executed on startup.
    Creates the users table if it doesn't exist.
    """
    create_users_table()


@app.post("/register")
def register(user: UserRegistration):
    """
    Endpoint for user registration.
    Validates the email and registers the user.
    """
    email = user.email
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email address format")
    if check_user_exists(email):
        raise HTTPException(status_code=400, detail="Email already registered")
    register_user(email)
    return {"message": "Registration successful"}


@app.post("/login")
def send_magic_link(magic_link: User):
    """
    Endpoint for sending a magic link for login.
    Validates the email, generates a token, and sends the magic link email.
    """
    email = magic_link.email
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email address format")
    if check_user_exists(email):
        token = TokenStorage.generate_token(email)
        TokenStorage.store_token(email, token)
        send_email(email, token)
        return {"message": "Magic link sent"}
    else:
        raise HTTPException(status_code=400, detail="Email address is not registered")


@app.get("/login/token={token}")
def login(token: str):
    """
    Endpoint for login using a token.
    Validates the token and performs the login operation.
    """
    if not token:
        raise HTTPException(status_code=400, detail="Token not provided")
    elif TokenStorage.validate_token(token):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
