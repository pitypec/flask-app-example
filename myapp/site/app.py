import os
import datetime
from flask import Blueprint, request
from myapp.extensions import bcrypt, db
from flask.json import jsonify
from myapp.utils import login_validator, signup_validator, allowed_file, protected_route, profile_validator
from werkzeug.utils import secure_filename
import jwt
from myapp.models import User, Userprofile, ProfileImage, Post, Comment, Friend, PostLike, CommentLike, Message
from myapp.extensions import socketio
from flask_socketio import emit
from myapp.status import *

site = Blueprint('site', __name__, template_folder='templates')

UPLOAD_FOLDER = '../images'
tokenkey = os.environ.get('TOKEN_KEY')


@site.route('/')
def index():
    return "<h1> Welcome to Social-Buzz</h1>"


@site.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = None
        parsejson = request.get_json()
        userdata = {
            "username": parsejson["username"],
            "password": parsejson["password"]

        }
        errors = login_validator(userdata)
        if errors is not None:
            for x in errors.values():
                return x
        data = User.query.filter((
            User.username == userdata['username']) | (User.email == userdata['username'])).first()
        if data is None:
            return jsonify({"Message": "User with email does not exist"}), HTTP_401_UNAUTHORIZED
        else:
            if data.password is not None:
                if bcrypt.check_password_hash(data.password, userdata['password']):
                    user = User.query.filter((User.username == userdata['username']) | (
                        User.email == userdata["username"])).first()
                try:
                    token = jwt.encode({"userid": user.id, "exp": datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=30)}, tokenkey).decode("utf8")
                except UnboundLocalError:
                    return jsonify({"Error": "Access denied"})

    return jsonify({
        "Message": "login successful",
        "token": token
    }), HTTP_200_OK


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
        errors = signup_validator(newuser_data)
        if errors is not None:
            for x in errors.values():
                return x
            checkuser = User.query.filter_by(
                username=newuser_data["username"]).first()
            if checkuser is not None:
                return jsonify({"Error": "username already exist"}), HTTP_400_BAD_REQUEST

            psw_hash = bcrypt.generate_password_hash(
                newuser_data['password']).decode("utf8")
            newuser = User(
                email=newuser_data["email"], username=newuser_data["username"], password=psw_hash)
            db.session.add(newuser)
            db.session.commit()
    return jsonify({"Message": "registration successful"}), HTTP_200_OK


@site.route('/profile', methods=['POST'])
@protected_route
def create_profile(current_user):
    if request.method == "POST":
        if current_user is not None:
            print(current_user)
            parsejson = request.get_json()
            newprofile = {
                "firstname": parsejson["firstname"],
                "middlename": parsejson["middlename"],
                "lastname": parsejson["lastname"],
                "location": parsejson["location"],
                "city": parsejson["city"],
                "user_id": current_user.id
            }
            errors = profile_validator(newprofile)
            if errors is not None:
                for x in errors.values():
                    return x
            user = User.query.get(current_user.id)
            profile = Userprofile(firstname=newprofile["firstname"], middlename=newprofile["middlename"], lastname=newprofile["lastname"],
                                  location=newprofile["location"], city=newprofile["city"], user_id=newprofile["user_id"], user=user)
            db.session.add(profile)
            db.session.commit()
            print(profile)
    return jsonify({"Message": "Profile saved"}), HTTP_200_OK


@site.route('/updateprofile', methods=['POST'])
@protected_route
def update_profile(current_user):
    if request.method == 'POST':
        parsejson = request.get_json()
        newprofile = {
            "firstname": parsejson["firstname"],
            "middlename": parsejson["middlename"],
            "lastname": parsejson["lastname"],
            "location": parsejson["location"],
            "city": parsejson["city"]
        }
        errors = profile_validator(newprofile)
        if errors is not None:
            for x in errors.values():
                return x
        print(current_user)
        profile = Userprofile.query.filter_by(
            user_id=current_user.id).first()
        print(profile)
        profile.firstname = newprofile["firstname"]
        profile.middlename = newprofile["middlename"]
        profile.lastname = newprofile["lastname"]
        profile.location = newprofile["location"]
        profile.city = newprofile["city"]
        db.session.commit()
    return jsonify({"Message": "Profile updated successfully"}), HTTP_200_OK


@site.route('/profile/<string:username>', methods=['GET'])
def friend_profile(username):
    try:
        user = User.query.filter_by(username=username).first()
    except TypeError:
        return jsonify({"Error": "user does not exist"})
    if user is None:
        return
    profile = Userprofile.query.filter_by(user_id=user.id).first()
    user_profile = {
        "firstname": profile.firstname,
        "middlename": profile.firstname,
        "lastname": profile.lastname,
        "location": profile.location,
        "city": profile.city,
        "username": profile.user.username,
        "email": profile.user.email
    }
    return jsonify(user_profile)


@site.route('/search', methods=['GET', 'POST'])
@protected_route
def search(current_user):
    if request.method == 'POST':
        search_list = {}
        parsejson = request.get_json()
        name = parsejson['search']
        user = Userprofile.query.filter((Userprofile.firstname.like("%{name}%")) |
                                        (Userprofile.lastname.like("%{name}%")) | (Userprofile.middlename.like('%{name}%'))).all()
        if user is None:
            return jsonify({"Error": f"user with {name} does not exist"})
        for x in user:
            search_list.append(x)
    return jsonify(search_list)


@site.route('/logout')
def logout():
    db.session.clear()
    return jsonify({"Message": "Logout Sucessful"})


@site.route('/post', methods=['POST'])
@protected_route
def create_post(current_user):
    if current_user is not None:
        if request.method == 'POST':
            parsejson = request.get_json()
            postdata = {
                "postbody": parsejson['body'],
                "post_image": parsejson['post_image']
            }
            user = User.query.get(current_user.id)
            post = Post(
                post_body=postdata['postbody'], post_image=postdata['post_image'], userposts=user)
            db.session.add(post)
            db.session.commit()
    return jsonify({"Message": "post successful"})


@site.route('/posts', methods=['GET'])
@protected_route
def get_all_posts(current_user):
    if current_user is not None:
        postlist = {}
        posts = User.query.filter_by(current_user.id).all()
        postlist.append(posts)
    return jsonify(postlist)


@site.route('/post/<int:id>', methods=['GET'])
@protected_route
def get_single_post(current_user, id):
    if current_user is not None:
        postlist = {}
        user = User.query.get(id)
        post = Post.query.filter(
            (Post.user_id == current_user.id), (Post.id == id))
        postlist.append(post)
    return jsonify(postlist)


@site.route('/comment', methods=['POST'])
@protected_route
def make_comment(current_user):
    if current_user is not None:
        if request.method == 'POST':
            parsejson = request.get_json()
            commentlist = {}
            newcomment = {
                "comment_body": parsejson['body']
            }
            postid = request.args['id']
            userid = current_user.id
            user = User.query.get(userid)
            username = user.username
            post = Post.query.filter_by(id=postid)
            comment = Comment(
                comment_body=newcomment['comment_body'], usercomment=user, postcomments=post)
            db.session.add(comment)
            db.session.commit()
    return jsonify(commentlist)


@site.route('/comments', methods=['GET'])
@protected_route
def get_all_comments(current_user, id):
    if current_user is not None:
        comments = {}
        postid = request.args['id']
        post = Post.query.filter_by(id=postid)
        comment = Comment.query.filter_by(post_id=postid)
        comments.append(comment)
    return jsonify(comments)


@site.route('/user', methods=['GET'])
def user(current_user):
    if current_user is None:
        return ""
    userdata = {}
    user = db.query.filter_by(id=current_user).first()
    userdata.append(user)
    return jsonify(userdata)


@site.route('/like/<int:id>', methods=['POST'])
@protected_route
def likes(current_user, id):
    if current_user is None:
        return
    poslikes = PostLike.query.filter_by(post_id=id).all()
    poslikes.number_of_like += 1
    return jsonify({"Message": "Liked"})


@site.route('/friends', methods=['GET'])
@protected_route
def get_all_friends(current_user):
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


@socketio.on('recieve message')
@protected_route
def message(current_user, data):
    if current_user is None:
        return
    message = Message.query.filter_by().all()
    emit('send message')
