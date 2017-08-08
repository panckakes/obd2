from flask import Flask, render_template, flash, redirect, url_for, request

from taskr import app, db, login_manager
from forms import SignupForm, TaskForm, LoginForm
from models import User, Task
from flask_login import login_required, login_user, logout_user, current_user
# import sys


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    user = User.query.all()
    return render_template('index.html', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Signed up successfully as {}.".format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/task', methods=['GET', 'POST'])
@login_required
def post_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        current_user.tasks.append(Task(title=title, description=description))
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('user_profile', username=current_user.username))
    tasks = Task.query.all()
    return render_template('tasks.html', form=form, tasks=tasks)


@app.route('/user/<username>')
def user_profile(username):
    # is the user logged in?
    if current_user.is_authenticated:
        pass
    # is this the logged in users profile?
    elif current_user.username == username:
        pass
    User.get_current_user()
    user = User.query.filter_by(username=username).first_or_404() # move to static method on user class
    # tasks = Task.current_user.query.filter_by(tasks=tasks)
    return render_template('user_profile.html', user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user_profile', username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
