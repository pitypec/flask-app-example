import os
import sys

from flask import Flask
from dotenv import load_dotenv
from .admin.app import admin
from .api.app import api
from .site.app import site
import myapp.config as config
from .extensions import bcrypt, db

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config.from_pyfile(config)
    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(admin)
    app.register_blueprint(api)
    app.register_blueprint(site)

    return app

# config_file='settings.py'
