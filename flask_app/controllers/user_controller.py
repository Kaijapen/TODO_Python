from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
@app.route("/login")
def start_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")