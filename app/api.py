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

    try:
        if page_nr is not None:
            page_nr = int(page_nr)
        else:
            page_nr = 1
    except ValueError:
        page_nr = 1
        info("Invalid page parameter {}".format(request.args.get('page')))

    events = Event.query.order_by(Event.start.desc()).paginate(page_nr, POSTS_PER_PAGE, False)

    return jsonify(map_paging_dto(events, [map_event_dto(event) for event in events.items]))


@app.route(create_api_uri("event/<int:event_id>"), methods=['GET'])
def get_event(event_id):
    event = Event.query.filter(Post.id == event_id).filter(Post.end >= datetime.now()).first()
    if event is None:
        print(request.headers)
        abort(404)
    else:
        return jsonify(map_event_dto(event))


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
