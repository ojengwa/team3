from flask import Blueprint

main = Blueprint('main', __name__)

from . import authentication, roles, frequencies, users, watchs, checks, errors
