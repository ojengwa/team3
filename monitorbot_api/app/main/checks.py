import json
import time

from flask import g, request, current_app, url_for
from ..models import Watch
from .. import db
from . import main
from .authentication import auth_user
from .errors import bad_request, unauthorized, forbidden, not_found


"""read all"""
@main.route('/<token>/checks/<int:watch_id>', methods=['GET'])                                   
def get_checks(token, watch_id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return all:
    checks = Check.query.filter_by(watch_id = watch_id).all()
    list_of_dicts = [json.loads(checks.to_json()) for check in checks]
    return json.dumps(list_of_dicts)


"""read one"""
@main.route('/<token>/checks/<int:id>/', methods=['GET'])
def get_check(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return one with id:
    check = Check.query.get(id)
    if check == None:
        not_found("Resource not found");
    return check.to_json()


# """create"""
# @main.route('/<token>/checks/', methods=['POST'])
# def new_check():
    # if not auth_user(token):
    #     return unauthorized("You have to be logged in to perform this action")

    # create and commit:
    # watch_id = request.form.get('frequency_id')
    # report = g.current_user.id
    # timestamp = time.time()
    # mail_sent = True

    # id = db.Column(db.Integer, primary_key=True)
    # watch_id = db.Column(db.Integer, db.ForeignKey('watchs.id'))
    # report = db.Column(db.String(64))
    # timestamp = db.Column(db.BigInteger)
    # mail_sent = db.Column(db.Boolean)

    # if url in ("", None) or frequency_id in ("", None):
    #     return bad_request("Invalid request format!")

    # watch = Watch( url=url, frequency_id=frequency_id, user_id=user_id, timestamp=timestamp, is_active=is_active )
    # db.session.add(watch)
    # db.session.commit()

    # # queue celery/broker:
    # queue_to_celery_broker(watch)

    # # run initial check:
    # run_check(watch.id)

    # # create and send response
    # response = {}
    # response["watch"] = watch.to_json()
    # response["status"] = "success"

    # return json.dumps(response)


# """delete"""
# @main.route('/<token>/watchs/<int:id>/', methods=["DELETE"])
# def update_user(token, id):
#     if not auth_user(token):
#         return unauthorized("You have to be logged in to perform this action")
    
#     watch = Watch.query.get(id)
#     if not watch:
#         not_found("Resource not found!")

#     # clear on celery/broker
#     clear_celery_broker(watch)

#     # delete and commit
#     db.session.delete(watch)
#     db.session.commit()

#     # queue celery/broker:
#     # delete_celery_broker(watch)

#     # ! delete associated checks!
#     # 

#     # create and send response
#     response = {}
#     response["status"] = "success"

#     return json.dumps(response)

        



