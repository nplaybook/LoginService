from flask import Flask
from flask_cors import CORS
from app.ext import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecret'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    register_extension(app)

    CORS(app)

    from app.routes.route import api
    app.register_blueprint(api)

    return app


def register_extension(app):
    db.init_app(app)