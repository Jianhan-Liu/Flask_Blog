"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/3/29
  Time: 15:21
 """
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from flaskblog import login_manager, db

__author__ = 'liujianhan'

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    _password = Column('password', String(128), nullable=False)
    image_file = Column(String(100), nullable=False, default='default.jpg')
    # TODO
    # posts = relationship(Post)
    posts = relationship('Post', backref='author', lazy=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_user_password(self, raw):
        return check_password_hash(self._password, raw)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class Post(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(30), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
