import json
from flask import g, jsonify, request, current_app, url_for
from ..models import User
from .. import db
from . import main
from .authentication import auth_user
from .errors import bad_request, unauthorized, forbidden, not_found



"""read all"""
@main.route('/<token>/users/', methods=['GET'])                                   
def get_users(token):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return all:
    users = User.query.all()
    list_of_dicts = [json.loads(user.to_json()) for user in users]
    return json.dumps(list_of_dicts)



"""read one"""
@main.route('/<token>/users/<int:id>/', methods=['GET'])
def get_user(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    # get and return one with id:
    user = User.query.get(id)
    if user == None:
        not_found("Resource not found");
    return user.to_json()


"""create"""
@main.route('/users/', methods=['POST']) #sign-up
def new_user():

    # create and commit user
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if  email in ("", None) or password in ("", None):
        return bad_request("Invalid request format!")

    user = User(username=username, email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()

    # get auth_token for the user:
    auth_token = user.generate_auth_token(3600*24)

    # create and send response
    response = {}
    response["user"] = user.to_json()
    response["auth_token"] = auth_token
    response["status"] = "success"

    return jsonify(response)



"""update"""
@main.route('/<token>/users/<int:id>/', methods=['PUT'])
def update_user(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")

    user = User.query.get(id)
    if not user:
        not_found("Resource not found!")

    # create and commit user
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if  email in ("", None) or password in ("", None):
        return bad_request("Invalid request format!")

    user.username = username
    user.email = email
    user.password = password

    db.session.add(user)
    db.session.commit()

    # create and send response
    response = {}
    response["user"] = user.to_json()
    response["status"] = "success"

    return jsonify(response)


"""delete"""
@main.route('/<token>/users/<int:id>/', methods=["DELETE"])
def delete_user(token, id):
    if not auth_user(token):
        return unauthorized("You have to be logged in to perform this action")
    
    user = User.query.get(id)
    if not user:
        not_found("Resource not found!")

    # delete and commit
    db.session.delete(user)
    db.session.commit()

    # ! delete associated watchs and checks!
    # 

    # create and send response
    response = {}
    response["status"] = "success"

    return json.dumps(response)



"""login"""
@main.route('/users/login/', methods=['POST'])
def login():

    # get credentials
    email = request.form.get('email')
    password = request.form.get('password')
    
    if  email in ("", None) or password in ("", None):
        return bad_request("Invalid request format!")

    # check for a user with matching credentials
    user = User.query.filter_by(email=email).first()
    if user == None or user.verify_password(password)==False:
        return bad_request("Invalid email or password!")

    # set the global current_user
    g.current_user = user
       
    # get auth_token for the user
    auth_token = user.generate_auth_token(3600*24) #1day
    
    # create response
    response =  {}
    response["user"] = user.to_json()
    response["auth_token"] = auth_token

    return jsonify(response)
        



