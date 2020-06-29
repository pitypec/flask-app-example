from flask import Blueprint

site = Blueprint('site', __name__, url_prefix='/site',
                 template_folder='templates')


@site.route('/')
def index():
    return '<h1>Welcome to site</h1>'
