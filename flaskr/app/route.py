from flask import Blueprint, render_template

view = Blueprint("views", __name__)

@view.get("/")
def index():
    return render_template("index.html")