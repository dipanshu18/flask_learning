from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = "SuPerSecReT"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///modularapp.db"

    db.init_app(app)

    @app.route("/")
    def index():
        uid = session.get("uid")
        if uid != None:
            return redirect(url_for("todos.get_todos"))

        return render_template("index.html")

    # import blueprint and register routes with prefixes
    from modularapp.blueprints.auth.routes import auth
    from modularapp.blueprints.todos.routes import todos

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(todos, url_prefix="/todos")

    Migrate(app, db)

    return app
