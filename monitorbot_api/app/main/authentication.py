
from flask import g
from ..models import User
from . import main

def auth_user(auth_token):
    g.current_user = User.verify_auth_token(auth_token)
    return g.current_user is not None



