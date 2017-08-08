from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
    url, ValidationError
from models import User, Task


# class BookmarkForm(Form):
#     url = URLField('The URL for your bookmark:', validators=[DataRequired(), url()])
#     description = StringField('Add an optional description:')


class SignupForm(FlaskForm):
    # username = StringField('Your Username people will see you as:', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(3, 80), Regexp('^[A-Za-z0-9_]{3,}$',
        message='Usernames consist of numbers, letters,''and underscores.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_validate', message='Passwords'
                                                                                                    ' must'' match.')])
    password_validate = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class TaskForm(FlaskForm):
    title = StringField()
    description = StringField()


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
