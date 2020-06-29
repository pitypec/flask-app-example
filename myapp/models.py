from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    middlename = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    joined_date = db.column(
        db.Datetime, default=datetime.utcnow, nullable=False)
    profile_picture = db.column(db.string, nullable=False)
    friends = db.relationship('Friend', backref='user', lazy=True)


class Friends(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    friends_list = db.Column(db.String, nullable=False)
    date_created = db.column(
        db.datetime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String, nullable=False)
    date_created = db.column(
        db.datetime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    date_created = db.Column(
        db.Datetime, default=datetime.utcnow, nullabe=False)


if __name__ == "__main__":
    db.create_all()
