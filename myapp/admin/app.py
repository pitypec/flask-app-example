from flask import Blueprint
from flask.json import jsonify
from myapp.models import User
from myapp.extensions import db, admin_user
from flask_login import logout_user, login_user
from flask_admin.contrib.sqla import ModelView

admin = Blueprint('admin', __name__, url_prefix='/admin',
                  template_folder='templates')


class MyModelView(ModelView):
    pass


admin_user.add_view(MyModelView(User, db.session))


@admin.route('/login')
def login():
    user = User.query.all()
    login_user(user)
    return jsonify({
        "Message": "Logged in"
    })


@admin.route('/logout')
def logout():
    logout_user()
    return jsonify({"Message": "Logout successful"})
