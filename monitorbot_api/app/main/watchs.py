import json
import time

from flask import g, request, current_app, url_for
from ..models import User, Watch, Check
from .. import db
from . import main
from .authentication import auth_user
from .tasks import run_check, queue_to_celery_broker #, update_celery_broker, clear_celery_broker
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
    frequency = request.form.get('frequency')
    user_id = g.current_user.id
    timestamp = time.time()
    is_active = True

    if url in ("", None) or frequency in ("", None):
        return bad_request("Invalid request format!")

    watch = Watch( url=url, frequency=frequency, user_id=user_id, timestamp=timestamp, is_active=is_active )
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
        return not_found("Resource not found!")

    # update and commit
    url = request.form.get('url')
    frequency = request.form.get('frequency')

    if url in ("", None) or frequency in ("", None):
        return bad_request("Invalid request format!")

    watch.url = url
    watch.frequency = frequency
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
        return not_found("Resource not found!")

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


"""create anony-watch"""
@main.route('/watchs/anony/', methods=['POST'])
def new_anony_watch():

    # create and commit:
    url = request.form.get('url')
    frequency = request.form.get('frequency')
    email = request.form.get('email')
    timestamp = time.time()
    is_active = True

    if url in ("", None) or frequency in ("", None) or email in ("", None):
        return bad_request("Invalid request format!")

    watch = Watch( url=url, frequency=frequency, email=email, timestamp=timestamp, is_active=is_active )
    db.session.add(watch)
    db.session.commit()

    # queue celery/broker:
    # queue_to_celery_broker(watch)

    # run initial check:
    init_check = run_check(watch.id)

    # create and send response
    response = {}
    response["watch"] = watch.to_json()
    response["init_check"] = init_check
    response["status"] = "success"

    return json.dumps(response)


"""delete anony-watch"""
@main.route('/watchs/anony/<int:id>/', methods=["DELETE"])
def delete_anony_watch(id):
    
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

        



