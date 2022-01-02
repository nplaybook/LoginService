import os
from hashlib import pbkdf2_hmac
from flaskr.app.models import User

def check_existing(username: str, email: str) -> bool: 
    """Check existing user from input usename and email.
    If user already exist will return False, otherwise True.
    
    :param username: {str} input username from request body
    :param email: {str} input email from request body
    
    :return: {bool}
    """

    user_data = User.query.filter_by(username=username, email=email).first()
    return user_data

def mask_password(password: str) -> tuple:
    """Mask password to database as salt and hash.

    :param password: {str} plain text password in request body
    
    :return: {tuple}
    """

    salt = os.urandom(32)
    hash = pbkdf2_hmac(
        hash_name="sha256", 
        password=password.encode("utf-8"), 
        salt=salt, 
        iterations=100_000
    )
    return salt, hash