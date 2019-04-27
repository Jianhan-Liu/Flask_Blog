"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/3/28
  Time: 19:38
 """
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail


__author__ = 'liujianhan'

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('flaskblog.config')

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

