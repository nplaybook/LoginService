from app.ext import db
from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    salt = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)

    def __init__(self, email: str, username: str, salt: str, hash: str) -> None:
        self.email = email
        self.username = username
        self.salt = salt
        self.hash = hash