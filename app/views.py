import random
import string
from datetime import datetime
from logging import info

from flask import render_template, flash, redirect, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_security import roles_required
from flask_security.utils import hash_password

from app import app, db, user_datastore
from app.email import password_reset_notification, new_account_notification
from app.forms import LoginForm, EditProfileForm, ChangePasswordForm, EditPostForm, EditEventForm, NewUserForm
from app.models import User, Post, Event
from config import POSTS_PER_PAGE


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', user=g.user)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        g.user.email = form.email.data
        g.user.phone = form.phone.data
        if form.city.data is not None and form.zipcode.data is not None and form.address.data is not None:
            g.user.city = form.city.data
            g.user.zipcode = form.zipcode.data
            g.user.address = form.address.data

        db.session.add(g.user)
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('profile'))
    else:
        form.first_name.data = g.user.first_name
        form.last_name.data = g.user.last_name
        form.email.data = g.user.email
        form.phone.data = g.user.phone
        form.city.data = g.user.city
        form.zipcode.data = g.user.zipcode
        form.address.data = g.user.address

    return render_template("edit_profile.html", form=form)


@app.route('/profile/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        g.user.password = form.new_password.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your password has been changed!')
        return redirect(url_for('profile'))

    return render_template("change_password.html", form=form)


@app.route('/blog')
@login_required
def blog():
    page = request.args.get('page')

    if page is None:
        return blog_index(1)
    else:
        try:
            return blog_index(page=int(page))
        except ValueError:
            info("Invalid page parameter {}".format(page))
            return blog_index(1)


@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = EditPostForm()

    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.timestamp = datetime.now()
        post.user_id = current_user.id
        db.session.add(post)
        db.session.commit()
        flash('Your blog post has been created!')
        return redirect(url_for('blog'))

    return render_template("create_post.html", form=form)


@app.route('/blog/<id>')
@login_required
def view_post(id):
    return render_template(
        'post_detail.html',
        post=Post.query.filter_by(id=id).first()
    )


@app.route('/blog/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = EditPostForm()
    post = Post.query.filter_by(id=id).first()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Your blog post has been changed!')
        return redirect(url_for('blog'))
    else:
        form.title.data = post.title
        form.body.data = post.body

    return render_template("edit_post.html", form=form)


@app.route('/blog/<int:id>/delete')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!')
    return blog_index(1)


def blog_index(page):
    return render_template(
        "blog.html",
        posts=Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    )


@app.route('/event')
@login_required
def events():
    page = request.args.get('page')

    if page is None:
        return events_index(1)
    else:
        try:
            return events_index(page=int(page))
        except ValueError:
            info("Invalid page parameter {}".format(page))
            return events_index(1)


@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
    form = EditEventForm()

    if form.validate_on_submit():
        kwb_event = Event()
        kwb_event.title = form.title.data
        kwb_event.description = form.description.data
        kwb_event.start = form.start.data
        kwb_event.end = form.end.data
        db.session.add(kwb_event)
        db.session.commit()
        flash('Your blog post has been created!')
        return redirect(url_for('events'))

    return render_template("create_event.html", form=form)


@app.route('/event/<id>')
@login_required
def view_event(id):
    return render_template(
        'event_detail.html',
        event=Event.query.filter_by(id=id).first()
    )


@app.route('/event/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    form = EditEventForm()
    kwb_event = Event.query.filter_by(id=id).first()

    if form.validate_on_submit():
        kwb_event.title = form.title.data
        kwb_event.description = form.description.data
        kwb_event.start = form.start.data
        kwb_event.end = form.end.data
        db.session.add(kwb_event)
        db.session.commit()
        flash('The event has been changed!')
        return redirect(url_for('events'))
    else:
        form.title.data = kwb_event.title
        form.description.data = kwb_event.description
        form.start.data = kwb_event.start
        form.end.data = kwb_event.end

    return render_template("edit_event.html", form=form)


@app.route('/event/<int:id>/delete')
@login_required
def delete_event(id):
    kwb_event = Event.query.filter_by(id=id).first()
    db.session.delete(kwb_event)
    db.session.commit()
    flash('Event has been deleted!')
    return events_index(1)


def events_index(page):
    return render_template(
        "events.html",
        events=Event.query.order_by(Event.start.desc()).paginate(page, POSTS_PER_PAGE, False)
    )


@app.route('/user')
@login_required
@roles_required('admin')
def users():
    page = request.args.get('page')
    page_nr = 1

    if page is not None:
        try:
            page_nr = int(page)
        except:
            info("Invalid page parameter {}".format(page))
            page_nr = 1

    return render_template("users.html",
                           page=User.query.order_by(User.last_name.asc(), User.first_name.asc()).paginate(page_nr,
                                                                                                          POSTS_PER_PAGE,
                                                                                                          False))


@app.route('/user/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def create_user():
    form = NewUserForm()
    password = generate_password()

    if form.validate_on_submit():
        user = User(
            form.first_name.data,
            form.last_name.data,
            hash_password(password),
            form.email.data
        )
        db.session.add(user)
        db.session.commit()
        new_account_notification(user, password)
        flash('User has been created!')
        return redirect(url_for('users'))

    return render_template('create_user.html', form=form)


@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def edit_user(id):
    return render_template('edit_user.html', user=User.query.filter_by(id=id).first())


@app.route('/user/<int:id>/password', methods=['GET'])
@login_required
@roles_required('admin')
def reset_password(id):
    new_password = generate_password()
    user = User.query.filter_by(id=id).first()
    user.password = hash_password(new_password)
    db.session.add(user)
    db.session.commit()
    password_reset_notification(user, new_password)
    flash('User password has been reset')
    return redirect(url_for('users'))


def generate_password():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))


@app.route('/user/<int:id>/deactivate', methods=['GET'])
@login_required
@roles_required('admin')
def deactivate_user(id):
    user = User.query.filter_by(id=id).first()
    user_datastore.deactivate_user(user)
    db.session.commit()
    flash('User deactivated')
    return redirect(url_for('users'))


@app.route('/user/<int:id>/activate', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def activate_user(id):
    user_datastore.activate_user(User.query.filter_by(id=id).first())
    db.session.commit()
    flash('User activated')
    return redirect(url_for('users'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.errorhandler(404)
def not_found_error(error):
    if request_wants_json():
        return jsonify({"message": "Resource Not Found"}), 404
    else:
        return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request_wants_json():
        return jsonify({"message": "Internal Server Error"}), 500
    else:
        return render_template('500.html'), 500


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
