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
            print(data["userid"])
            current_user = User.query.filter_by(id=data["userid"]).first()
            print(current_user)
        except:
            return jsonify({"message": "Token is invalid"})
        return f(current_user, *args, **kwargs)
    return decorated


def login_validator(data):
    errors = {}
    if data["username"].isspace():
        errors["username"] = jsonify(
            {"Error": "please enter a valid username"})
    elif len(data["username"]) <= 0:
        errors["username"] = jsonify({"Error": "field cannot be empty"})
    if data["password"].isspace():
        errors["password"] = jsonify({"Error": "please enter your password"})
    elif len(data["password"]) <= 0:
        errors["password"] = jsonify(
            {"Error": "password field cannot be empty"})
    return errors


def signup_validator(data):
    errors = {}
    if data["email"].isspace():
        errors["email"] = jsonify({"error": "please enter a valid email"})
    elif len(data["email"]) <= 0:
        errors["email"] = jsonify({"Error": "field cannot be empty"})
    if data["username"].isspace():
        errors["username"] = jsonify(
            {"Error": "Please enter a valid username"})
    elif len(data["username"]) <= 0:
        errors["username"] = jsonify({"Error": "field cannot be empty"})
    if data["password"].isspace():
        errors["password"] = jsonify({"Error": "Please enter a password"})
    elif len(data["password"]) <= 0:
        errors["password"] = jsonify({"Error": "field cannot be empty"})
    if data["confirmpassword"] != data["password"]:
        errors["confirmpassword"] = jsonify({"Error": "Password must match"})
    return errors


def profile_validator(data):
    errors = {}
    if data["firstname"].isspace():
        errors["firstname"] = jsonify(
            {"Error": "Please enter a valid firstname"})
    elif len(data["firstname"]) <= 0:
        errors["middlesname"] = jsonify({"Error": "field cannot be empty"})
    if data["middlename"].isspace():
        errors["middlename"] = jsonify(
            {"Error": "Please enter a valid middlename"})
    elif len(data["middlename"]) <= 0:
        errors["middlename"] = jsonify({"Error": "field cannot be empty"})
    if data["lastname"].isspace():
        errors["lastname"] = jsonify(
            {"Error": "Please enter a valid lastname"})
    elif len(data["lastname"]) <= 0:
        errors["lastname"] = jsonify({"Error": "field cannot be empty"})
    if data["location"].isspace():
        errors["location"] = jsonify(
            {"Error": "Please enter a valid location"})
    elif len(data["location"]) <= 0:
        errors["location"] = jsonify({"Error": "field cannot be empty"})
    if data["city"].isspace():
        errors["city"] = jsonify({"Error": "Please enter a valid city"})
    elif len(data["city"]) <= 0:
        errors["city"] = jsonify({"Error": "field cannot be empty"})
    return errors


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
