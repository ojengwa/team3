import json
import time

from flask import g, request, current_app, url_for
from ..models import User, Watch, Check
from .. import db
from . import main
from .authentication import auth_user
from .errors import bad_request, unauthorized, forbidden, not_found


"""read all"""
@main.route('/<token>/watchs/', methods=['GET'])                                   
def get_watchs(token):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return all:
    watchs = Watchs.query.filter_by(user = g.current_user).all()
    list_of_dicts = [json.loads(watch.to_json()) for watch in watchs]
    return json.dumps(list_of_dicts)


"""read one"""
@main.route('/<token>/watchs/<int:id>/', methods=['GET'])
def get_watch(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return one with id:
    watch = Watchs.query.get(id)
    if watch == None:
        not_found("Resource not found");
    return watch.to_json()


"""create"""
@main.route('/<token>/watchs/', methods=['POST'])
def new_watch(token):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")

    # create and commit:
    url = request.form.get('url')
    frequency_id = request.form.get('frequency_id')
    user_id = g.current_user.id
    timestamp = time.time()
    is_active = True

    if url in ("", None) or frequency_id in ("", None):
        return bad_request("Invalid request format!")

    watch = Watch( url=url, frequency_id=frequency_id, user_id=user_id, timestamp=timestamp, is_active=is_active )
    db.session.add(watch)
    db.session.commit()

    # queue celery/broker:
    queue_to_celery_broker(watch)

    # run initial check:
    run_check(watch.id)

    # create and send response
    response = {}
    response["watch"] = watch.to_json()
    response["status"] = "success"

    return json.dumps(response)


"""update"""
@main.route('/<token>/watchs/<int:id>/', methods=['PUT'])
def update_watch(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    
    watch = Watch.query.get(id)
    if not watch:
        not_found("Resource not found!")

    # update and commit
    url = request.form.get('url')
    frequency_id = request.form.get('frequency_id')

    if url in ("", None) or frequency_id in ("", None):
        return bad_request("Invalid request format!")

    watch.url = url
    watch.frequency_id = frequency_id
    watch.timestamp = time.time()

    db.session.add(watch)
    db.session.commit()

    # queue celery/broker:
    update_celery_broker(watch)

    # run initial check:
    run_check(watch.id)

    # create and send response
    response = {}
    response["watch"] = watch.to_json()
    response["status"] = "success"

    return json.dumps(response)


"""delete"""
@main.route('/<token>/watchs/<int:id>/', methods=["DELETE"])
def delete_watch(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    
    watch = Watch.query.get(id)
    if not watch:
        not_found("Resource not found!")

    # clear on celery/broker
    clear_celery_broker(watch)

    # delete and commit
    db.session.delete(watch)
    db.session.commit()

    # queue celery/broker:
    # delete_celery_broker(watch)

    # ! delete associated checks!
    # 

    # create and send response
    response = {}
    response["status"] = "success"

    return json.dumps(response)

        



