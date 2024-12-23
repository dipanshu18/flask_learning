from flask import request, session, render_template, redirect, flash, url_for, Blueprint
from modularapp.blueprints.auth.models import User
from modularapp.app import db

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/register", methods=["GET", "POST"])
def register():
    uid = session.get("uid")

    if uid != None:
        return redirect(url_for("todos/index.html"))

    if request.method == "GET":
        return render_template("auth/register.html")
    elif request.method == "POST":
        name = request.form.get("name")
        user_email = request.form.get("email")
        password = request.form.get("password")

        user_exists = User.query.filter(User.email == user_email).first()

        if user_exists:
            flash("User already exists with these credentials. Kindly login")
            return render_template("auth/register.html")

        new_user = User(name=name, email=user_email)
        new_user.hash_password(password)

        db.session.add(new_user)
        db.session.commit()

        session["uid"] = new_user.id

        return redirect(url_for("todos.get_todos"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    uid = session.get("uid")

    if uid != None:
        return redirect(url_for("todos.get_todos"))

    if request.method == "GET":
        return render_template("auth/login.html")
    elif request.method == "POST":
        user_email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == user_email).first()

        if user == None:
            flash("User does not exists with these credentials, kindly register")
            return render_template("auth/login.html")

        if user and user.check_password(password):
            session["uid"] = user.id
            return redirect(url_for("todos.get_todos"))
        else:
            flash("Incorrect credentials!")
            return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    uid = session.get("uid")

    if uid == None:
        flash("Unauthorized, kindly login to access this route")
        return redirect(url_for("auth.login"))

    session.pop("uid")
    return redirect(url_for("index"))
