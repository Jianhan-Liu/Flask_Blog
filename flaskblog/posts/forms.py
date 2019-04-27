"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/4/3
  Time: 0:49
 """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

__author__ = 'liujianhan'


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
