import os
from flask import Blueprint, request
from myapp.extensions import bcrypt
from flask.json import jsonify
from myapp.utils import login_validator, signup_validator, allowed_file, protected_route
from werkzeug.utils import secure_filename


site = Blueprint('site', __name__, url_prefix='/site',
                 template_folder='templates')

UPLOAD_FOLDER = '../images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@site.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        parsejson = request.get_json()
        userdata = {
            "username": parsejson["username"],
            "password": parsejson["password"],
            "confirmpassword": parsejson["confirmpassword"]
        }
        login_validator(userdata)

    return '<h1>Welcome to site</h1>'


@site.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        parsejson = request.get_json()
        newuser_data = {
            "username": parsejson["username"],
            "email": parsejson["email"],
            "password": parsejson["password"],
            "confirmpassword": parsejson["confirmpassword"]
        }
        signup_validator(newuser_data)
    return '<h1>Welcome to site</h1>'


@site.route('/user', methods=['POST'])
def user():
    return '<h1>Welcome to site</h1>'


@site.route('/logout')
def logout():
    return '<h1>Welcome to site</h1>'


@site.route('/likes')
def likes():
    return '<h1>Welcome to site</h1>'


@site.route('/comments')
def comments():
    return '<h1>Welcome to site</h1>'


@site.route('/comment')
def comment():
    return '<h1>Welcome to site</h1>'


@site.route('/posts')
def posts():
    return '<h1>Welcome to site</h1>'


@site.route('/post')
def post():
    return '<h1>Welcome to site</h1>'


@site.route('/friends')
def friends():
    return '<h1>Welcome to site</h1>'


@site.route('/profileimage', methods=['GET', 'POST'])
def upload_profile_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"Error": "no file attached"})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"Error": "No file part"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            new_image = Image(
                path=UPLOAD_FOLDER,
                filename=filename,
                ext=filename.rsplit('.', 1)[1].lower()
            )
            # Save new_image model
            return jsonify({"Message": "Image uploded successfully"})
