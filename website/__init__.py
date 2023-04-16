from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .view import view
from .authorization import auth


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Leha_secret"

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
