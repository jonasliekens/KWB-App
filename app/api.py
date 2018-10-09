from datetime import datetime
from logging import info

from flask import jsonify, request
from flask_sqlalchemy import Pagination
from werkzeug.exceptions import abort

from app import app
from app.models import Event, Post, User
from config import POSTS_PER_PAGE


def create_api_uri(uri):
    return "/api/1_0/{}".format(uri)


@app.route(create_api_uri("event"), methods=['GET'])
def get_events():
    page_nr = request.args.get('page')
    from_date = request.args.get('fromDate')

    try:
        if page_nr is not None:
            page_nr = int(page_nr)
        else:
            page_nr = 1
    except ValueError:
        page_nr = 1
        info("Invalid page parameter {}".format(request.args.get('page')))

    if from_date:
        events = Event.query\
            .filter(Event.start >= datetime.strptime(from_date, "%d/%m/%Y"))\
            .order_by(Event.start.asc())\
            .paginate(page_nr, POSTS_PER_PAGE, False)
    else:
        events = Event.query.order_by(Event.start.asc()).paginate(page_nr, POSTS_PER_PAGE, False)

    return jsonify(map_paging_dto(events, [map_event_dto(event) for event in events.items]))


@app.route(create_api_uri("event/next"))
def get_first_upcoming():
    upcoming_event = Event.query.filter(Event.start >= datetime.now()).order_by(Event.start.asc()).first()

    if upcoming_event:
        return jsonify(map_event_dto(upcoming_event))
    else:
        upcoming_event = Event()
        upcoming_event.description = 'Er zijn geen activiteiten meer ingeplant!'
        upcoming_event.title = 'Coming soon'
        upcoming_event.start = datetime.now()
        return jsonify(map_event_dto(upcoming_event))


@app.route(create_api_uri("event/<int:event_id>"), methods=['GET'])
def get_event(event_id):
    event = Event.query.filter(Event.id == event_id).first()
    if event is None:
        print(request.headers)
        abort(404)
    else:
        return jsonify(map_event_detail_dto(event))


@app.route(create_api_uri("post"), methods=['GET'])
def get_posts():
    page_nr = request.args.get('page')

    try:
        if page_nr is not None:
            page_nr = int(page_nr)
        else:
            page_nr = 1
    except ValueError:
        page_nr = 1
        info("Invalid page parameter {}".format(request.args.get('page')))

    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page_nr, POSTS_PER_PAGE, False)

    return jsonify(map_paging_dto(posts, [map_post_dto(post) for post in posts.items]))


@app.route(create_api_uri("post/<int:post_id>"), methods=['GET'])
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        abort(404)
    else:
        return jsonify(map_post_dto(post))


@app.route(create_api_uri("post/latest"))
def get_latest_post():
    post = Post.query.order_by(Post.timestamp.desc()).first()

    if post:
        return jsonify(map_post_dto(post))
    else:
        post = Post()
        post.timestamp = datetime.now()
        post.title = 'Coming soon'
        post.body = 'Voorlopig is er nog niets gepost!'
        return jsonify(map_post_dto(post))


def map_user_dto(user: User):
    return {
        "firstName": user.first_name,
        "lastName": user.last_name,
        "address": user.address,
        "city": user.city,
        "zipCode": user.zipcode,
        "phone": user.phone,
        "email": user.email,
        "avatar": user.avatar(150)
    }


@app.route(create_api_uri("user"), methods=['GET'])
def get_users():
    return jsonify([map_user_dto(user) for user in User.query.all()])


def map_paging_dto(page: Pagination, items):
    return {
        "hasNext": page.has_next,
        "hasPrev": page.has_prev,
        "next_num": page.next_num,
        "prev_num": page.prev_num,
        "page": page.page,
        "pages": page.pages,
        "per_page": page.per_page,
        "total": page.total,
        "items": items
    }


def map_post_dto(post: Post):
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "timestamp": post.timestamp.strftime('%d-%m-%Y %H:%M:%S')
    }


def map_event_dto(event: Event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.start.strftime('%d-%m-%Y')
    }


def map_event_detail_dto(event: Event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "start": event.start.strftime('%d-%m-%Y %H:%M:%S'),
        "end": event.end.strftime('%d-%m-%Y %H:%M:%S'),
        "location": event.location
    }
