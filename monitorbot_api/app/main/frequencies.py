import json
import time

from flask import g, request, current_app, url_for
from ..models import Frequency
from .. import db
from . import main
from .authentication import auth_user
from .errors import bad_request, unauthorized, forbidden, not_found


"""read all"""
@main.route('/<token>/frequencies/', methods=['GET'])                                   
def get_frequencies(token):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return all:
    frequencies = Frequencies.query.all()
    list_of_dicts = [json.loads(frequency.to_json()) for frequency in frequencies]
    return json.dumps(list_of_dicts)


"""read one"""
@main.route('/<token>/frequencies/<int:id>/', methods=['GET'])
def get_frequency(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return one with id:
    frequency = Frequencies.query.get(id)
    if frequency == None:
        not_found("Resource not found");
    return frequency.to_json()


"""create"""
@main.route('/<token>/frequencies/', methods=['POST'])
def new_frequency(token):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")

    # create and commit:
    name = request.form.get('name')
    value = request.form.get('value')

    if name in ("", None) or value in ("", None):
        return bad_request("Invalid request format!")

    frequency = Frequency( name=name, value=value)
    db.session.add(frequency)
    db.session.commit()

    # create and send response
    response = {}
    response["frequency"] = frequency.to_json()
    response["status"] = "success"

    return json.dumps(response)


"""delete"""
@main.route('/<token>/frequencies/<int:id>/', methods=["DELETE"])
def delete_frequency(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    
    frequency = Frequency.query.get(id)
    if not frequency:
        not_found("Resource not found!")

    # create and send response
    response = {}
    response["status"] = "success"

    return json.dumps(response)

        



