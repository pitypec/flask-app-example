from flask import Blueprint
from flask.views import MethodView

api = Blueprint('api', __name__, url_prefix='/api',
                template_folder='templates')


# @api.route('/')
# def index():
#     return "<h1> Welcome to api</h1>"
