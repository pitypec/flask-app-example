from flask import Blueprint
from flask.views import MethodView

api = Blueprint('api', __name__, template_folder='templates')


class User(MethodView):
    def get(self):
        return 'returned a user'

    def post(self):
        return 'Created an user'

    def put(self):
        return 'Modified a user'

    def delete(self):
        return 'Deleted an user'


@api.route('/')
def index():
    return '<h1>Welcome to api</h1>'
