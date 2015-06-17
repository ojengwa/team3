from flask import g, jsonify, request, current_app, url_for
from authentication import auth_user
from ..models import User, Post

"""read all"""
@main.route('/<str:token>/users/', methods=['GET'])                                   
def get_users(token):
    if  auth_user(token):
        users = User.query.all()
        return jsonify( [user.to_json() for user in users] )

"""read one"""
@main.route('/<str:token>/users/<int:id>', methods=['GET'])
def get_user(token, id):
    if  auth_user(token):
        user = User.query.get_or_404(id)
        return user.to_json()

"""create"""
@main.route('/signup/', methods=['POST'])
def get_user(token):
    if  auth_user(token):

        user = User()
        return user.to_json()



