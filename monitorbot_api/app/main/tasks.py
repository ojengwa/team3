import json
import time

from flask import g, request, current_app, url_for
from ..models import User, Watch, Check
from .. import db
from . import main
from .authentication import auth_user
from .errors import bad_request, unauthorized, forbidden, not_found


"""celery task function"""
@main.route('/<token>/celery/<watch_id>', methods=['GET'])                                   
def run_checks(watch_id):
    clear_celery_broker(watch)



