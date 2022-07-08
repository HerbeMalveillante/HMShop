from this import d
from flask import Blueprint, render_template, request, flash
import re


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
    return render_template("login.html", boolean=True)


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password = request.form.get("password")

        valid = True

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
            flash("Account created. Please log in.", category="success")

    return render_template("sign_up.html")
