from flask import Blueprint, request, session, jsonify
from marshmallow import ValidationError

from flaskr import db
from flaskr.app.models.user import User
from flaskr.app.utils.validator import UserRegister, UserLogin, UserResetPassword
from flaskr.app.utils.auth import (
    check_existing_user, mask_password, match_password, 
    issue_jwt, get_user_data, token_required
)
from flaskr.app.utils.response import generate_response

api = Blueprint("api", __name__)


@api.post("/user/login")
def login():
    try:
        request_data: dict = UserLogin().load(request.form)
        is_exist: bool = check_existing_user(email=request_data['email'])
        # CASE: USER NOT IN THE DATABASE
        if not is_exist:
            message: str = "User not found"
            return jsonify(generate_response(http_status=404, message=message)), 404
        user_data: dict = get_user_data(email=request_data["email"])
        is_password_match: bool = match_password(password=request_data["password"], salt=user_data.salt, hash=user_data.hash)
        # CASE: WRONG PASSWORD
        if not is_password_match:
            message: str = "Password not match"
            return jsonify(generate_response(http_status=404, message=message)), 404
        token: dict = issue_jwt(data=user_data, expired_minutes=60)
        session["token"] = token
        message: str = "Login success"
        return jsonify(generate_response(http_status=200, message=message, data={"token": token})), 200
    except ValidationError as val_err:
        return jsonify(generate_response(http_status=400, message=val_err.messages)), 400
    except Exception as error:
        return jsonify(generate_response(http_status=500,message=error)), 500


@api.post("/user/signup")
def signup():
    try:
        request_data: dict = UserRegister().load(request.form)
        is_exist: bool = check_existing_user(email=request_data["email"], username=request_data["username"])
        if is_exist:
            message: str = "Email/Username already registered"
            return jsonify(generate_response(http_status=404, message=message)), 404
        salt, hash = mask_password(password=request_data["password"])
        new_user = User(
            email=request_data["email"],
            username=request_data["username"],
            salt=salt,
            hash=hash
        )
        db.session.add(new_user)
        db.session.commit()
        message: str = "New account is registered"
        return jsonify(generate_response(http_status=200, message=message)), 200
    except ValidationError as val_err:
        return jsonify(generate_response(http_status=400, message=val_err.messages)), 400
    except Exception as error:
        return jsonify(generate_response(http_status=500, message=error)), 500


@api.post("/user/logout")
@token_required
def logout(user):
    try:
        if "token" in session:
            session.pop("token", None)
        message: str = "You have successfully logged out"
        return jsonify(generate_response(http_status=200, message=message)), 200
    except Exception as error:
        return jsonify(generate_response(http_status=500, message=error)), 500


@api.post("/user/reset")
def reset():
    # TODO: IMPROVE SECURITY BY SENDING EMAIL USING FLASK-MAIL
    try:
        request_data: dict = UserResetPassword().load(request.form)
        is_exist: bool = check_existing_user(email=request_data["email"], username=request_data["username"])
        # CASE: VALIDATE INPUT EMAIL AND USERNAME
        if not is_exist:
            message: str = "Wrong email/username"
            return jsonify(generate_response(http_status=404, message=message)), 404
        salt, hash = mask_password(password=request_data["password"])
        user: dict = get_user_data(email=request_data["email"])
        user.salt, user.hash = salt, hash
        db.session.commit()
        message: str = "Password is updated"
        return jsonify(generate_response(http_status=200, message=message)), 200
    except ValidationError as val_err:
        return jsonify(generate_response(http_status=400, message=val_err.messages)), 400
    except Exception as error:
        return jsonify(generate_response(http_status=500, message=error)), 500