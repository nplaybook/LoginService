from flask import Blueprint, render_template, request, redirect
import os
import sqlite3

view = Blueprint("views", __name__)
api = Blueprint("api", __name__)

@view.get("/")
def index():
    return "Index"

@view.get("/login")
def login():
    return render_template("login.html")

@api.get("/signup")
def signup():
    return "Signup"

@api.get("/logout")
def logout():
    return "Logout"