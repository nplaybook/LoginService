from flask import Flask
from flask_cors import CORS

from app.ext import db
from app.routes.route import api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db.init_app(app)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run()