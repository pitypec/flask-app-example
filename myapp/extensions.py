from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
admin_user = Admin()
loginmanager = LoginManager()
