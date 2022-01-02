from flask import Blueprint, request, jsonify
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
        request_data = UserLogin().load(request.json)
        user_data = check_existing_user(email=request_data['email'])
        if user_data is None:
            return generate_response(http_status=400, message="Email is not registered")
        match_status = match_password(password=request_data["password"], salt=user_data.salt, hash=user_data.hash)
        if match_status == False:
            return generate_response(http_status=400, message="Wrong password") 
        token = issue_jwt(data=user_data, expired_minutes=60)
        return jsonify(generate_response(
            http_status=200, 
            message="Login success", 
            data=token
        ))
    except ValidationError as val_err:
        response = generate_response(http_status=400, message=val_err.messages)
        return jsonify(response)
    except Exception as error:
        response = generate_response(http_status=500,message=error)
        return jsonify(response)

@api.post("/user/signup")
def signup():
    try:
        request_data = UserRegister().load(request.json)
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
        return jsonify(generate_response(
            http_status=200, 
            message="Successfully registered user", 
            data=request_data 
        ))
    except ValidationError as val_err:
        response = generate_response(http_status=400, message=val_err.messages)
        return jsonify(response)
    except Exception as error:
        response = generate_response(http_status=500, message=error)
        return jsonify(response)