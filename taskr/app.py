import os

from datetime import datetime

from flask_wtf.csrf import CSRFProtect
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template, flash, redirect, url_for, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from logging import DEBUG
from forms import UserForm
# import models


# basedir = os.path.abspath(os.path.dirname(__file__))


# app = Flask(__name__)
# app.logger.setLevel(DEBUG)
# csrf = CSRFProtect(app)

# app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'taskr.db')
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

users = []


# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)


# def store_users(email, password):
#     users.append(dict(
#         email = email,
#         password = password,
#         date = datetime.utcnow()
#     ))
#
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)