from flask import Flask
from sqlalchemy.sql import func
from datetime import datetime
from .extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    join_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    userprofile = db.relationship('Userprofile', backref='user', uselist=False)
    posts = db.relationship('Post', backref='userposts', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.id


class Userprofile(db.Model):
    __tablename__ = "userprofile"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))
    profileimage = db.relationship(
        'ProfileImage', backref='userprofile', uselist=False)


class ProfileImage(db.Model):
    __tablename__ = "profileimage"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'userprofile.id'), nullable=False)


class Friend(db.Model):
    __tablename__ = "friend"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    friend = db.relationship('User', foreign_keys=[friend_id])
    became_friends = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    sent_from = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sent_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    user = db.relationship('User', foreign_keys=[sent_from])
    friend = db.relationship('User', foreign_keys=[sent_to])
    date_sent = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_body = db.Column(db.String(500), nullable=False)
    post_image = db.Column(db.String(500), nullable=True)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    comments = db.relationship(
        'Comment', backref='postcomments', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    Comment_like = db.Column(db.Integer, default=0, nullable=False)
    comment_body = db.Column(db.String, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class PostLike(db.Model):
    __tablename__ = "postlike"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    numberof_like = db.Column(db.Integer, default=0, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class CommentLike(db.Model):
    __tablename__ = "commentlike"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_id = db.Column(
        db.Integer, db.ForeignKey('post.id'), nullable=False)
    numberof_like = db.Column(db.Integer, default=0, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
