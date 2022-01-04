from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from marshmallow import ValidationError

from flaskr import db
from flaskr.app.models.user import User
from flaskr.app.utils.validator import UserRegister, UserLogin
from flaskr.app.utils.auth import (
    check_user_login, check_user_signup, mask_password, 
    match_password, issue_jwt, get_user_data
)
from flaskr.app.utils.response import generate_response

api = Blueprint("api", __name__)

@api.post("/user/login")
def login():
    try:
        request_data = UserLogin().load(request.form)
        is_exist = check_user_login(email=request_data['email'])
        if is_exist:
            flash("User is not registered")
            return redirect(url_for("views.login"))
        user_data = get_user_data(email=request_data["email"])
        is_password_match = match_password(password=request_data["password"], salt=user_data.salt, hash=user_data.hash)
        if not is_password_match:
            flash("Password is incorrect")
            return redirect(url_for("views.login"))
        token = issue_jwt(data=user_data, expired_minutes=60)
        response = generate_response(http_status=200, message="Login success", data={"token": token})
        return render_template("chat.html", response=response)
    except ValidationError as val_err:
        response = generate_response(http_status=400, message=val_err.messages)
        return jsonify(response)
    except Exception as error:
        response = generate_response(http_status=500,message=error)
        return jsonify(response)

@api.post("/user/signup")
def signup():
    try:
        request_data = UserRegister().load(request.form)
        is_exist = check_user_signup(email=request_data["email"], username=request_data["username"])
        if is_exist:
            flash("Email/Username already registered", "error")
            return redirect(url_for("views.signup"))
        salt, hash = mask_password(password=request_data["password"])
        new_user = User(
            email=request_data["email"],
            username=request_data["username"],
            salt=salt,
            hash=hash
        )
        db.session.add(new_user)
        db.session.commit()
        flash("New account is registered", "message")
        return redirect(url_for("views.signup"))
    except ValidationError as val_err:
        response = generate_response(http_status=400, message=val_err.messages)
        return jsonify(response)
    except Exception as error:
        response = generate_response(http_status=500, message=error)
        return jsonify(response)