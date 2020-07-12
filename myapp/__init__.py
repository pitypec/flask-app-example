import os
import sys

from flask import Flask
from dotenv import load_dotenv
from .admin.app import admin
from .api.app import api
from .site.app import site
import myapp.config as config
from .extensions import bcrypt, db, admin_user, loginmanager


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    bcrypt.init_app(app)
    admin_user.init_app(app)
    loginmanager.init_app(app)
    app.register_blueprint(admin)
    app.register_blueprint(api)
    app.register_blueprint(site)

    return app

    # load_dotenv()
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
