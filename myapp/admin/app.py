from flask import Blueprint
from flask.json import jsonify
from myapp.models import User
from myapp.extensions import db, admin, loginmanager
from flask_login import logout_user, login_user
from flask_admin.contrib.sqla import ModelView

adminbp = Blueprint('adminbp', __name__, url_prefix='/admin',
                    template_folder='templates')


@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class MyModelView(ModelView):
    pass


@adminbp.route('/login')
def login():
    user = User.query.all()
    login_user(user)
    return jsonify({
        "Message": "Logged in"
    })


@adminbp.route('/logout')
def logout():
    logout_user()
    return jsonify({"Message": "Logout successful"})


admin.add_view(MyModelView(User, db.session))
