"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/4/3
  Time: 0:48
 """
from flaskblog.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestRestForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email

__author__ = 'liujianhan'

from flask import Blueprint
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user, login_user, logout_user

from flaskblog.models import Post, db, User

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        # TODO
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register success! Now you are ready to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_user_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_url = request.args.get('next')
            # 防止重定向攻击
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('main.home')
            return redirect(next_url)
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form, title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).\
        order_by(Post.date_posted.desc()).\
        paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! Now you are ready to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
