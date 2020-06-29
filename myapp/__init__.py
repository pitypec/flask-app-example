import os

from flask import Flask
from .admin.app import admin
from .api.app import api
from .site.app import site
from .models import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config_from_object(config_object)
    db.init_app(app)
    app.register_blueprint(admin)
    app.register_blueprint(api)
    app.register_blueprint(site)

    return app
