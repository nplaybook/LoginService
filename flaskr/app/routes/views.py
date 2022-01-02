from flask import Blueprint, render_template

view = Blueprint("views", __name__)

@view.get("/")
def index():
    return "Index"

@view.get("/login")
def login():
    return render_template("login.html")

@view.get("/signup")
def view_signup():
    return render_template("signup.html")