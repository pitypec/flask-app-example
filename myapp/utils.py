import requests

from flask import request
from flask.json import jsonify
import jwt
from functools import wraps
from .models import db


def protected_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"message": "A valid token is required"})
        try:
            data = jwt.decode(token, tokenKey)
            print(data)
            current_user = db.execute("SELECT * FROM users WHERE user_id = :user_id",
                                      {"user_id": data['userid']}).first()
            db.commit()
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
    if data["username"].isspace():
        return jsonify({"Error": "Please enter a valid username"})
    elif len(data["username"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["email"].isspace():
        return jsonify({"Error": "Please enter a valid email"})
    elif len(data["email"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["password"].isspace():
        return jsonify({"Error": "Please enter a password"})
    elif len(data["password"]) <= 0:
        return jsonify({"Error": "field cannot be empty"})
    if data["confirmpassword"] != data["password"]:
        return jsonify({"Error": "Password must match"})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
