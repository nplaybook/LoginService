from marshmallow import ValidationError
from flask import Blueprint, render_template, request, redirect, jsonify
from flaskr import db
from flaskr.app.models import User
from flaskr.app.validator import UserRegister
from flaskr.app.controller import user as user_function
from flaskr.app.utils.response import generate_response

view = Blueprint("views", __name__)
api = Blueprint("api", __name__)

@view.get("/")
def index():
    return "Index"

@view.get("/login")
def login():
    return render_template("login.html")

@view.get("/signup")
def view_signup():
    return render_template("signup.html")

@api.post("/user/signup")
def api_signup():
    try:
        request_data = UserRegister().load(request.json)
        user_data = user_function.check_existing(
            username=request_data["username"], 
            email=request_data["email"])
        if user_data is not None: return "Username or Email already registered"
        salt, hash = user_function.mask_password(password=request_data["password"])
        new_user = User(
            email=request_data["email"],
            username=request_data["username"],
            salt=salt,
            hash=hash
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(generate_response(
            http_status=200, 
            message="Successfully registered user", 
            data=request_data 
        ))
    except ValidationError as val_err:
        response = generate_response(
            http_status=400,
            message=val_err.messages
        )
        return jsonify(response)
    except Exception as error:
        response = generate_response(
            http_status=500,
            message=error
        )
        return jsonify(response)


# @api.get("/user")
# def get_user():
#     result = User.query.get(1)