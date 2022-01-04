import os
import jwt
from datetime import datetime, timedelta
from hashlib import pbkdf2_hmac
from flask import current_app
from flaskr.app.models.user import User

def check_user_login(email: str) -> bool: 
    """Check existing user login info from input usename and email.
    If user already exist will return True, otherwise False.
    
    :param email: {str} input email from request body
    
    :return: {bool}
    """

    validation: bool = False

    validate_email = User.query.filter_by(email=email).first()
    validation = True if validate_email is None else False
 
    return validation

def check_user_signup(email: str, username: str) -> bool: 
    """Check existing user signup info from input usename and email.
    If user already exist will return True, otherwise False.
    
    :param username: {str} input username from request body
    :param email: {str} input email from request body
    
    :return: {bool}
    """

    validation: bool = True
    
    validate_username = User.query.filter_by(username=username).first()
    validation = True if validate_username is not None else False
    if validation: return validation
    

    validate_email = User.query.filter_by(email=email).first()
    validation = True if validate_email is not None else False
 
    return validation

def get_user_data(email: str) -> dict:
    """Query user data by corresponding email.
    
    :param email: {str} from input form
    :return: {dict}
    """
    
    user_data = User.query.filter_by(email=email).first()
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

def match_password(password: str, salt: str, hash: str) -> bool:
    """Match password from request body and salt-hash pair
    in the database. Return True if input password and
    salt-hash pair decoded password (from hash) is similar, otherwise False.
    
    :param password: {str} password from request body
    :param salt: {str} salt bytes from database
    :param hash: {str} hash bytes from database
    
    :return: {bool}
    """

    generated_hash = pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=100_000
    )

    return True if generated_hash == hash else False

def issue_jwt(data: dict, expired_minutes: int) -> dict:
    """Create JWT for authentication purpose.
    
    :param data: {dict} input data from request body
    :param expired_minutes: {int} jwt expired date after n-minutes
    the token is created

    :return: {dict}
    """

    token = jwt.encode({
        "user": data.username, 
        "exp": datetime.utcnow() + timedelta(minutes=expired_minutes)
    }, key=current_app.config["SECRET_KEY"])
    return token