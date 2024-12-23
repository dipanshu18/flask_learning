from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from models import User


def register_routes(app: Flask, db: SQLAlchemy):
    @app.route("/")
    def index():
        email = session.get("email")

        if email:
            return redirect(url_for("home"))

        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            email = session.get("email")

            if email:
                return redirect(url_for("home"))

            return render_template("auth/login.html")
        elif request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user: User = User.query.filter(User.email == email).first()

            if user == None:
                flash("User not found with these credentials. Kindly signup!")
                return render_template("auth/login.html")

            if user and user.check_password(password):
                session["email"] = email
                return redirect(url_for("home"))
            else:
                flash("Incorrect credentials!")
                return render_template("auth/login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            email = session.get("email")

            if email:
                return redirect(url_for("home"))

            return render_template("auth/register.html")
        elif request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            user_exists: User = User.query.filter(User.email == email).first()
            if user_exists:
                flash("User already exists with these credentials. Kindly login!")
                return render_template("auth/register.html")

            user = User(name=name, email=email)
            user.hash_password(password)

            session["email"] = email

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("home"))

    @app.route("/logout")
    def logout():
        if session["email"]:
            session.pop("email")
            return redirect(url_for("index"))

        return flash("Unauthorized access")

    @app.route("/home")
    def home():
        email = session.get("email")

        if email == None:
            return redirect(url_for("login"))

        user = User.query.filter(User.email == email).first()
        print(user)
        return render_template("dashboard/home.html", user=user)
