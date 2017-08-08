from taskr import app, db
from flask_script import prompt_bool
from flask_script import Manager as DB_Manager
from flask_migrate import Migrate, MigrateCommand

from taskr.models import *

manager = DB_Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="michael", email="panckakes@gmail.com", password="grampo"))

    # db.session.add(User(username="arjen", email="arjen@example.com", password="test"))

    db.session.commit()
    print 'Initialized the database'


@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'


if __name__ == '__main__':
    manager.run()