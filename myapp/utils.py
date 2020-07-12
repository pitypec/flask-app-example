import requests
import os
from flask import request
from flask.json import jsonify
import jwt
from functools import wraps
from .extensions import db
from .models import User

tokenkey = os.environ.get('TOKEN_KEY')


def protected_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"message": "A valid token is required"})
        try:
            data = jwt.decode(token, tokenkey)
            print(data)
            current_user = db.Query.filter_by(id=data['userid']).first()
            db.session.commit()
        except:
            return jsonify({"message": "Token is invalid"})
        return f(current_user, *args, **kwargs)
    return decorated


def login_validator(data):
    if data["email"].isspace():
        return jsonify({"Error": "please enter a valid email"})
    elif len(data["email"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["password"].isspace():
        return jsonify({"Error": "please enter your password"})
    elif len(data["password"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})


def signup_validator(data):
    if data["email"].isspace():
        return jsonify({"Error": "Please enter a valid email"})
    elif len(data["email"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["username"].isspace():
        return jsonify({"Error": "Please enter a valid username"})
    elif len(data["username"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["firstname"].isspace():
        return jsonify({"Error": "Please enter a valid email"})
    elif len(data["firstname"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["middlename"].isspace():
        return jsonify({"Error": "Please enter a valid email"})
    elif len(data["middlename"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["lastname"].isspace():
        return jsonify({"Error": "Please enter a valid email"})
    elif len(data["lstname"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["password"].isspace():
        return jsonify({"Error": "Please enter a password"})
    elif len(data["password"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["confirmpassword"] != data["password"]:
        return jsonify({"Error": "Password must match"})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
