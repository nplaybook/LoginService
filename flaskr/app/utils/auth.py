import os
from datetime import datetime, timedelta
from hashlib import pbkdf2_hmac
from functools import wraps

import jwt
from flask import current_app, request, session, jsonify

from flaskr.app.models.user import User
from flaskr.app.utils.response import generate_response


def check_existing_user(email: str, username: str=None):
    """Check existing user info from input email and usename (optional).
    If user already exist will return True, otherwise False.
    
    :param email: {str} input email from request body
    :param username: {str} input username from request body
    :return: {bool}
    """

    validation: bool = True

    validate_email = User.query.filter_by(email=email).first()
    validation = validate_email is not None

    if username:
        validate_username = User.query.filter_by(username=username).first()
        validation = validate_username is not None

    return validation


def get_user_data(email: str) -> dict:
    """Query user data by corresponding email.
    
    :param email: {str} from input form
    :return: {dict}
    """
    
    return User.query.filter_by(email=email).first()


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

    return generated_hash == hash


def issue_jwt(data: dict, expired_minutes: int) -> dict:
    """Create JWT for authentication purpose.
    
    :param data: {dict} input data from request body
    :param expired_minutes: {int} jwt expired date after n-minutes
    the token is created

    :return: {dict}
    """

    return jwt.encode({
        "username": data.username,
        "email": data.email,
        "exp": datetime.utcnow() + timedelta(minutes=expired_minutes)
    }, key=current_app.config["SECRET_KEY"])


def token_required(func):
    """Decorator that will ensure the visiting route
    can be accessed only by authenticated user
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        elif "token" in session:
            token = session["token"]
        
        if not token:
            response = generate_response(http_status=401, message="Token is missing")
            return jsonify(response), 401

        try:
            data = jwt.decode(token, key=current_app.config["SECRET_KEY"])
            user = User.query.filter_by(username=data["username"]).first()
        except:
            response = generate_response(http_status=401, message="Token is invalid")
            return jsonify(response), 401

        return func(user, *args, **kwargs)
    return decorated