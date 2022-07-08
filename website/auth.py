from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import re
from flask_login import login_user, login_required, logout_user, current_user


def valid_email(email):
    if len(email) > 7:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
    return False


def valid_password(password):
    """a valid password must contain at least 8 characters, and a special character."""
    if len(password) > 7:
        if re.match(
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,}).*", password
        ):
            return True
    return False


def valid_firstName(firstName):
    if len(firstName) >= 2:
        return True
    return False


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("You are now logged in.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))

            else:
                flash("Invalid password. Try again.", category="error")
        else:
            flash("User not found. Try again.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password = request.form.get("password")

        valid = True

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists.", category="error")
            valid = False
        if not valid_email(email):
            flash("Email is not valid.", category="error")
            valid = False
        if not valid_firstName(firstName):
            flash("First name must be at least 2 characters long", category="error")
            valid = False
        if not valid_password(password):
            flash(
                "Password must be at least 8 characters long, and contain a special character.",
                category="error",
            )
            valid = False
        if valid:
            # add user to the database
            new_user = User(
                email=email,
                first_name=firstName,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created. Please log in.", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
