from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api',
                template_folder='templates')


@api.route('/')
def index():
    return '<h1>Welcome to api</h1>'
