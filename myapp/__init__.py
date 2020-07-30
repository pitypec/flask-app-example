import os
import sys

from flask import Flask
from dotenv import load_dotenv
from .admin.app import adminbp as admin_blueprint
from .api.app import api, User
from .site.app import site
from .extensions import bcrypt, db, admin, loginmanager, socketio
from .commands import create_tables


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    socketio.init_app(app)
    loginmanager.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(site)
    app.register_blueprint(admin_blueprint)
    app.cli.add_command(create_tables)
    # app.add_url_rule('/user', view_func=User.as_view('user'))

    return app

    # load_dotenv()
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
