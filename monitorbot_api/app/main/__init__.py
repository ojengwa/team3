from flask import Blueprint

main = Blueprint('main', __name__)

from . import authentication, errors, users, watchs  #, roles, frequencies,  , checks
