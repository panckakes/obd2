import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging import DEBUG
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from settings import *


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
csrf = CSRFProtect(app)

# Configure database
app.config['SECRET_KEY'] = '~t\x86\xc9i\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+settings.DB_USER+':'+settings.DB_PASS+'@'+settings.DB_URL+'/'+settings.DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)


import taskr.models
import taskr.views
