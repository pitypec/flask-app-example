from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin',
                  template_folder='templates')


@admin.route('/')
def index():
    return '<h1>Welcome to admin</h1>'
