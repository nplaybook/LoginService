from flask import Blueprint, request, render_template, flash, redirect, url_for
from marshmallow import ValidationError

from flaskr import db
from flaskr.app.models.user import User
from flaskr.app.utils.validator import UserRegister, UserLogin
from flaskr.app.utils.auth import (
    check_existing_user, mask_password, 
    match_password, issue_jwt
)
from flaskr.app.utils.response import generate_response

api = Blueprint("api", __name__)

@api.post("/user/login")
def login():
    try:
        request_data = UserLogin().load(request.form)
        user_data = check_existing_user(email=request_data['email'])
        if user_data is None:
            flash("User is not registered")
            return redirect(url_for("views.login"))
        match_status = match_password(password=request_data["password"], salt=user_data.salt, hash=user_data.hash)
        if match_status == False:
            return generate_response(http_status=400, message="Wrong password") 
        token = issue_jwt(data=user_data, expired_minutes=60)
        response = generate_response(http_status=200, message="Login success", data={"token": token})
        return render_template("chat.html", response=response)
    except ValidationError as val_err:
        response = generate_response(http_status=400, message=val_err.messages)
        return response
    except Exception as error:
        response = generate_response(http_status=500,message=error)
        return response

@api.post("/user/signup")
def signup():
    try:
        request_data = UserRegister().load(request.form)
        user_data = check_existing_user( email=request_data["email"])
        if user_data is not None: 
            return generate_response(http_status=400, message="Email is already registered")
        salt, hash = mask_password(password=request_data["password"])
        new_user = User(
            email=request_data["email"],
            username=request_data["username"],
            salt=salt,
            hash=hash
        )
        db.session.add(new_user)
        db.session.commit()
        response = generate_response(http_status=200, message="Successfully registered user") 
        return render_template("login.html", response=response)
    except ValidationError as val_err:
        response = generate_response(http_status=400, message=val_err.messages)
        return response
    except Exception as error:
        response = generate_response(http_status=500, message=error)
        return response