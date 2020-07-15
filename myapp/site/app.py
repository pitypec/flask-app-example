import os
import datetime
from flask import Blueprint, request
from myapp.extensions import bcrypt, db
from flask.json import jsonify
from myapp.utils import login_validator, signup_validator, allowed_file, protected_route
from werkzeug.utils import secure_filename
import jwt
from myapp.models import User

site = Blueprint('site', __name__, url_prefix='/site',
                 template_folder='templates')

UPLOAD_FOLDER = '../images'
tokenkey = os.environ.get('TOKEN_KEY')


@site.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        parsejson = request.get_json()
        userdata = {
            "email": parsejson["email"],
            "password": parsejson["password"],
        }
        login_validator(userdata)
        data = User.query.filter_by(email=userdata['username']).first()
        token = ""
        if data is None:
            return jsonify({"Message": "User with email does not exist"})

        else:
            for psw_data in data['password']:
                if bcrypt.check_password_hash(psw_data, userdata['password']):
                    user = User.query.filter_by(email=userdata['email'])
                token = token = jwt.encode({"userid": user.id, "exp": datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=30)}, tokenkey)
                token = token.decode("utf-8")
        db.session.commit()
    return jsonify({
        "Message": "login successful",
        "token": token
    })


@site.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        parsejson = request.get_json()
        newuser_data = {
            "email": parsejson["email"],
            "username": parsejson["username"],
            "firstname": parsejson["firstname"],
            "middlename": parsejson["middlename"],
            "lastname": parsejson["lastname"],
            "password": parsejson["password"],
            "confirmpassword": parsejson["confirmpassword"]
        }
        signup_validator(newuser_data)
        psw_hash = bcrypt.generate_password_hash(
            newuser_data['password']).decode("utf8")
        newuser = User(email=newuser_data["email"], username=newuser_data["username"], firstname=newuser_data["firstname"],
                       middlename=newuser_data["middlename"], lastname=newuser_data["lastname"], password=psw_hash)
        db.session.add(newuser)
        db.session.commit()
    return jsonify({"Message": "registration successful"})


@site.route('/user', methods=['GET'])
@protected_route
def user(current_user):
    if current_user is None:
        return ""
    userdata = db.query.filter_by(id=current_user)
    return '<h1>Welcome to site</h1>'


@site.route('/logout')
def logout():
    db.session.clear()
    return jsonify({"Message": "Logout Sucessful"})


# @site.route('/likes')
# @protected_route
# def likes(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/comments')
# @protected_route
# def comments(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/comment')
# @protected_route
# def comment(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/posts')
# @protected_route
# def posts(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/post')
# @protected_route
# def post(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/friends')
# @protected_route
# def friends(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/profileimage', methods=['GET', 'POST'])
# @protected_route
# def upload_profile_image(current_user):
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             return jsonify({"Error": "no file attached"})
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             return jsonify({"Error": "No file part"})
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             new_image = ProfileImage(
#                 path=UPLOAD_FOLDER,
#                 filename=filename,
#                 ext=filename.rsplit('.', 1)[1].lower()
#             )
#             db.session.add(new_image)
#             db.session.commit()
#     return jsonify({"Message": "Image uploded successfully"})
