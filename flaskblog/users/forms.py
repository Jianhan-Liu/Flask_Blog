"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/4/3
  Time: 0:49
 """
from flask_login import current_user
from flask_wtf.file import FileAllowed

from flaskblog.models import User

__author__ = 'liujianhan'
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # @staticmethod
    # 此处必须写为validate_something
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Validation error, the username has been taken')

    # @staticmethod
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Validation error, the email has been taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, field):
        if field.data != current_user.username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError('Validation error, the username has been taken')

    # @staticmethod
    def validate_email(self, field):
        if field.data != current_user.email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError('Validation error, the email has been taken')


class RequestRestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Your must reigister first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
