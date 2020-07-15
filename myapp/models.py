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
    # posts = db.relationship('Post', backref='user_post', lazy=True)

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


# class Post(db.Model):
#     __tablename__ = "post"
#     # __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     post_body = db.Column(db.String(500), nullable=False)
#     date_created = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     comments = db.relationship(
#         'Comment', backref='postcomments', lazy='dynamic')
#     post_image = db.relationship(
#         'PostImage', backref='postimage', lazy='dynamic')


# class PostImage(db.Model):
#     __tablename__ = "postimage"
#     id = db.Column(db.Integer, primary_key=True)
#     path = db.Column(db.String(500), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# class Comment(db.Model):
#     __tablename__ = "comment"
#     id = db.Column(db.Integer, primary_key=True)
#     comment_body = db.Column(db.String, nullable=False)
#     date_created = db.Column(
#         db.DateTime, default=datetime.utcnow, nullabe=False)
#     user_id = db.Column(db.Integer, db.ForiegnKey('user.id'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)


# class PostLike(db.Model):
#     __tablename__ = "postlike"
#     like_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.Foreignkey('user.id'), nullable=False)
#     post_id = db.Column(db.Integer, db.Foreignkey('post.id'), nullable=False)
#     numberof_like = db.Column(db.Integer, nullable=False)
#     date_created = db.Column(
#         db.DateTime, default=datetime.utcnow, nullabe=False)


# class CommentLike(db.Model):
#     __tablename__ = "commentlike"
#     like_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.Foreignkey('user.id'), nullable=False)
#     comment_id = db.Column(
#         db.Integer, db.Foreignkey('post.id'), nullable=False)
#     numberof_like = db.Column(db.Integer, nullable=False)
#     date_created = db.Column(
#         db.DateTime, default=datetime.utcnow, nullabe=False)
