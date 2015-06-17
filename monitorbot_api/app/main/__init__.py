from flask import Blueprint

main = Blueprint('main', __name__)

from . import authentication , users#, roles, frequencies,  watchs, checks, errors
