"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/4/3
  Time: 0:48
 """
from flaskblog.models import Post

__author__ = 'liujianhan'

from flask import Blueprint, request, render_template

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About Page')
