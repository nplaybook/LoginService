from flask import Blueprint, request, session, jsonify
from marshmallow import ValidationError

from app.ext import db
from app.models.user import User
from app.utils.validator import UserRegister, UserLogin, UserResetPassword
from app.utils.auth import (
    check_existing_user, mask_password, match_password, 
    issue_jwt, get_user_data, token_required, validate_password_req
)
from app.utils.response import generate_response


api = Blueprint("api", __name__, url_prefix="/api/auth/")

@api.post("/login")
def login():
    try:
        request_data: dict = UserLogin().load(request.json)
        is_exist: bool = check_existing_user(email=request_data['email'])
        # CASE: USER NOT IN THE DATABASE
        if not is_exist:
            return jsonify(generate_response(http_status=404, message="User not found")), 404
        user_data: User = get_user_data(email=request_data["email"])
        is_password_match: bool = match_password(password=request_data["password"], salt=user_data.salt, hash=user_data.hash)
        # CASE: WRONG PASSWORD
        if not is_password_match:
            return jsonify(generate_response(http_status=404, message="Password not match")), 404
        token: dict = issue_jwt(data=user_data, expired_minutes=60)
        session["token"] = token
        return jsonify(generate_response(http_status=200, message="Login success", data={"token": token})), 200
    except ValidationError as val_err:
        return jsonify(generate_response(http_status=400, message=val_err.messages)), 400
    except Exception as error:
        return jsonify(generate_response(http_status=500,message=error)), 500


@api.post("/signup")
def signup():
    try:
        request_data: dict = UserRegister().load(request.json)
        is_exist: bool = check_existing_user(email=request_data["email"], username=request_data["username"])
        if not is_exist:
            return jsonify(generate_response(http_status=404, message="Email/Username already registered")), 404
        is_password_validated: bool = validate_password_req(password=request_data["password"])
        if not is_password_validated:
            return jsonify(generate_response(http_status=404, message="Password at least contain lowercase, uppercase, symbol, and number")), 404
        salt, hash = mask_password(password=request_data["password"])
        new_user: User = User(
            email=request_data["email"],
            username=request_data["username"],
            salt=salt,
            hash=hash
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(generate_response(http_status=200, message="New account is registered")), 200
    except ValidationError as val_err:
        return jsonify(generate_response(http_status=400, message=val_err.messages)), 400
    except Exception as error:
        return jsonify(generate_response(http_status=500, message=error)), 500


@api.post("/logout")
@token_required
def logout(user):
    try:
        if "token" in session:
            session.pop("token", None)
        return jsonify(generate_response(http_status=200, message="You have successfully logged out")), 200
    except Exception as error:
        return jsonify(generate_response(http_status=500, message=error)), 500


@api.post("/reset")
def reset():
    # TODO: IMPROVE SECURITY BY SENDING EMAIL USING FLASK-MAIL
    try:
        request_data: dict = UserResetPassword().load(request.json)
        is_exist: bool = check_existing_user(email=request_data["email"], username=request_data["username"])
        # CASE: VALIDATE INPUT EMAIL AND USERNAME
        if not is_exist:
            return jsonify(generate_response(http_status=404, message= "Wrong email/username")), 404
        salt, hash = mask_password(password=request_data["password"])
        user: dict = get_user_data(email=request_data["email"])
        user.salt, user.hash = salt, hash
        db.session.commit()
        return jsonify(generate_response(http_status=200, message="Password is updated")), 200
    except ValidationError as val_err:
        return jsonify(generate_response(http_status=400, message=val_err.messages)), 400
    except Exception as error:
        return jsonify(generate_response(http_status=500, message=error)), 500