import os
import datetime
from flask import Blueprint, request
from myapp.extensions import bcrypt, db
from flask.json import jsonify
from myapp.utils import login_validator, signup_validator, allowed_file, protected_route, profile_validator
from werkzeug.utils import secure_filename
import jwt
from myapp.models import User, Userprofile, ProfileImage, Post, Comment, Friend, PostLike, CommentLike
from myapp.extensions import socketio
from flask_socketio import emit

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
        data = User.query.filter(and_(
            User.username == userdata['username'], User.password == userdata['password'])).first()
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
            "password": parsejson["password"],
            "confirmpassword": parsejson["confirmpassword"]
        }
        signup_validator(newuser_data)
        psw_hash = bcrypt.generate_password_hash(
            newuser_data['password']).decode("utf8")
        newuser = User(
            email=newuser_data["email"], username=newuser_data["username"], password=psw_hash)
        db.session.add(newuser)
        db.session.commit()
    return jsonify({"Message": "registration successful"})


@site.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        parsejson = request.get_json()
        newprofile = {
            "firstname": parsejson["firstname"],
            "middlename": parsejson["middlename"],
            "lastname": parsejson["lastname"],
        }
        profile_validator(newprofile)
        profile = Userprofile(
            firstname=newprofile['firstname'], middlename=newprofile['middlename'], lastname=['lastname'])
        db.session.add(profile)
        db.session.commit()
        return jsonify({"Message": "Profile updated successfully"})


@site.route('/profile/<int:id>', methods=['GET'])
def friend_profile(parameter_list):
    userprofile = Userprofile.query.get(id).all()
    return jsonify(userprofile)


@site.route('/user', methods=['GET'])
def user(current_user):
    if current_user is None:
        return ""
    userdata = {}
    user = db.query.filter_by(id=current_user).first()
    userdata.append(user)
    return jsonify(userdata)


@site.route('/logout')
def logout():
    db.session.clear()
    return jsonify({"Message": "Logout Sucessful"})


@site.route('/post', methods=['POST'])
def post(parameter_list):
    if request.method == 'POST':
        parsejson = request.get_json()
        postdata = {
            "postbody": parsejson['body'],
            "post_image": parsejson['post_image']
        }
    pass


@site.route('/posts')
@protected_route
def posts(current_user):
    postlist = {}
    posts = Post.query.get(current_user).order_by(Post.date_created).all()
    postlist.append(posts)
    return jsonify(postlist)


@site.route('/post/<int:id>')
@protected_route
def posts(current_user, id):
    postlist = {}
    posts = Post.query.get(id).all()
    postlist.append(posts)
    return jsonify(postlist)


@site.route('/comments')
@protected_route
def comments(current_user):
    commentlist = {}
    comments = Comment.query.get(current_user).order_by(
        Comment.date_created).all()
    commentlist.append(comments)
    return jsonify(commentlist)


@site.route('/like/<int:id>')
@protected_route
def likes(current_user, id):
    if current_user is None:
        return
    poslikes = PostLike.query.filter_by(post_id=id).all()
    poslikes.number_of_like += 1
    return jsonify({"Message": "Liked"})


# @site.route('/comment')
# @protected_route
# def comment(current_user):
#     return '<h1>Welcome to site</h1>'


# @site.route('/post')
# @protected_route
# def post(current_user):
#     return '<h1>Welcome to site</h1>'


@site.route('/friends')
@protected_route
def friends(current_user):
    if current_user is None:
        return
    friendslist = Friend.query.filter_by(user_id=current_user).all()
    return jsonify(friendslist)


@site.route('/profileimage', methods=['GET', 'POST'])
@protected_route
def upload_profile_image(current_user):
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
            new_image = ProfileImage(
                path=UPLOAD_FOLDER,
                filename=filename,
                ext=filename.rsplit('.', 1)[1].lower()
            )
            db.session.add(new_image)
            db.session.commit()
    return jsonify({"Message": "Image uploaded successfully"})


# @socketio.on('recieve message')
# def message(data):
#     emit('send message')
