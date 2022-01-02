from datetime import datetime
from flaskr import app, db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    salt = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, email: str, username: str, salt: str, hash: str) -> None:
        self.email = email
        self.username = username
        self.salt = salt
        self.hash = hash