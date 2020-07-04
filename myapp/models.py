from flask import Flask
from sqlalchemy.sql import func
from datetime import datetime
from .extensions import db


# tags = db.Table('tags',
#                 db.Column('user_id', db.Integer,
#                           db.ForeignKey('user.user_id')),
#                 db.Column('friend_id', db.Integer,
#                           db.Foreignkey('friend.friend_id'))
#                 )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    middlename = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    join_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    posts = db.relationship('Post', backref='user_post', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.id

    # friend_sender = db.relationship(
    #     'Post', primaryjoin='User.user_id == Friend.friend_id', backref='request_sender', lazy='dynamic')
    # friend_receiver = db.relationship(
    #     'Post', foreign_keys='User.id == Post.moderated_by', backref='post_blame', lazy='dynamic')


class Friend(db.Model):
    __tablename__ = "friend"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend = db.relationship('User', foreign_keys=[friend_id])
    became_friends = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class Post(db.Model):
    __tablename__ = "post"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    post_body = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=True)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship('Comment', backref='associated_comments')


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.String, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullabe=False)
    post = db.Column(db.Integer, db.Foreignkey("post.id"), nullable=False)


# class Like(db.Model):
#     __tablename__ = "Like"
#     like_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     Comment_id = db.column(db.Integer, nullable=False)
#     post_id = db.Column(db.Integer, nullable=False)
#     number_of_like = db.Column(db.Integer, nullable=False)
#     date_created = db.Column(
#         db.DateTime, default=datetime.utcnow, nullabe=False)


if __name__ == "__main__":
    db.create_all()
