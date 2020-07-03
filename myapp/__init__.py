import os

from flask import Flask
from dotenv import load_dotenv
from .admin.app import admin
from .api.app import api
from .site.app import site
import myapp.config as config
from .extensions import bcrypt, db


def create_app(config):
    app = Flask(__name__)
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config_from_object(config)
    db.init_app(app)
    bcrypt.init_app(app)
    print(os.getenv("DATABASE_URL"))
    app.register_blueprint(admin)
    app.register_blueprint(api)
    app.register_blueprint(site)

    return app
