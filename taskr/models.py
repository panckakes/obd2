from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


teams = db.Table('teams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    # db.Column('organization_id', db.Integer, db.ForeignKey('organization.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)


organizations = db.Table('organizations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)


# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
#     db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
# )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    # possibly a temp email for schools or internal emails
    secondary_email = db.Column(db.String(80))
    password_hash = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    # Signup date
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # type = db.Column(db.String(30))

    # organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    # users = db.Column(db.Integer, db.ForeignKey('user.id'))

    organizations = db.relationship('Organization', secondary=organizations, backref=db.backref('users', lazy='dynamic'))
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    # tags = db.relationship('Tag', secondary=tags, backref=db.backref('Tag', lazy='dynamic'))

    # __mapper_args__ = {
    #     'polymorphic_identity': 'user',
    #     'polymorphic_on': type
    # }

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_current_user(username):
        return User.query.filter_by(username=username).first_or_404()

    def __repr__(self):
        return "<User '{}'>".format(self.username)


# class Admin(User):
#     id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#
#     __mapper_args__ = {
#             'polymorphic_identity': 'admin',
#         }


# class Manager(User):
#     id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     clock_in = db.Column(db.DateTime, default=datetime.utcnow)
#     clock_out = db.Column(db.DateTime, default=datetime.utcnow)
#
#     # tags = db.relationship('Tag', secondary=tags, backref=db.backref('Task', lazy='dynamic'))
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'manager',
#     }


# class Employee(User):
#     id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     clock_in = db.Column(db.DateTime, default=datetime.utcnow)
#     clock_out = db.Column(db.DateTime, default=datetime.utcnow)
#
#     # tags = db.relationship('Tag', secondary=tags, backref=db.backref('Task', lazy='dynamic'))
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'employee',
#     }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(140), unique=True)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    # task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    # tags = db.relationship('Tag', secondary=tags, backref=db.backref('Task', lazy='dynamic'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(20), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # sub_tasks =
    # prerequisites = db.Column()
    due_date = db.Column(db.DateTime, default=datetime.utcnow)
    work_hrs_required = db.Column(db.Integer)
    task_assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    task_start_date = db.Column(db.DateTime, default=datetime.utcnow)
    task_due_date = db.Column(db.DateTime, default=datetime.utcnow)
    task_completed_date = db.Column(db.DateTime, default=datetime.utcnow)

    # _tags = db.relationship('Tag', secondary=tags, lazy='joined',
    #                         backref=db.backref('task', lazy='dynamic'))

    #tags = db.relationship('Tag', secondary=tags, backref=db.backref('Task', lazy='dynamic'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    # @property
    # def tags(self):
    #     return ", ".join([t.name for t in self._tags])
    #
    # @property
    # def tag_list(self):
    #     return [t.name.strip() for t in self._tags]
    #
    # @tags.setter
    # def tags(self, string):
    #     if string:
    #         self._tags = [Tag.get_or_create(name.strip()) for name in string.split(',')]

    def __repr__(self):
        return "<task '{}'>".format(self.title)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))

    users = db.relationship('User', secondary=teams, backref=db.backref('User', lazy='dynamic'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))

    # users = db.Column(db.Integer, db.ForeignKey('user.id'))
    # teams = db.Column(db.Integer, db.ForeignKey('team.id'))


# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30))
#     color = db.Column(db.String(6))
#
#     @staticmethod
#     def get_or_create(name):
#         try:
#             return Tag.query.filter_by(name=name).one()
#         except:
#             return Tag(name=name)