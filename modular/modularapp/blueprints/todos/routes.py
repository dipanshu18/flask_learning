from flask import request, render_template, redirect, url_for, session, flash, Blueprint
from modularapp.app import db
from modularapp.blueprints.todos.models import Todo
from modularapp.blueprints.auth.models import User

todos = Blueprint("todos", __name__, template_folder="templates")


@todos.route("/")
def get_todos():
    uid = session.get("uid")

    if uid == None:
        flash("Unauthorized, kindly login to access this route")
        return redirect(url_for("auth.login"))

    loggedin_user = User.query.filter(User.id == uid).first()
    todos = Todo.query.filter(Todo.user_id == uid)

    return render_template("todos/index.html", todos=todos, username=loggedin_user.name)


@todos.route("/create", methods=["GET", "POST"])
def create_todo():
    uid = session.get("uid")

    if uid == None:
        flash("Unauthorized, kindly login to access this route")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("todos/create.html")
    elif request.method == "POST":
        loggedin_user = User.query.filter(User.id == uid).first()

        title = request.form.get("title")
        description = request.form.get("description")
        done = True if "done" in request.form.keys() else False

        description = description if description != "" else None

        new_todo = Todo(
            title=title, description=description, done=done, user=loggedin_user
        )

        db.session.add(new_todo)
        db.session.commit()

        flash("Created todo")

        return redirect(url_for("todos.get_todos"))
