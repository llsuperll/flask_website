from flask import Flask
from data import db_session
from view import view
from authorization import auth

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Leha_secret"
    db_session.global_init(f"db/{DB_NAME}")

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.run()

    return app
