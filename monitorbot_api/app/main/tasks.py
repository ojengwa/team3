import json
import time
import requests

from flask import g, request, current_app, url_for
from ..models import User, Watch, Check
from .. import db
from . import main
from .authentication import auth_user
from .errors import bad_request, unauthorized, forbidden, not_found

from flask.ext.mail import Message
from threading import Thread
from .. import mail

# from celery import Celery
def queue_to_celery_broker(watch):
    pass

@main.route('/tasks/check/<watch_id>/', methods=['GET'])                                   
def run_check(watch_id):
    
    watch = Watch.query.get(watch_id)
    if not watch:
        # clear_celery_broker(watch_id)
        return not_found("Resource not found!")

    # check if site is available:
    r = requests.get(watch.url)
    timestamp = time.time()

    if r.status_code == 200:             # the site is available:
        report = "[AVAILABLE] The site at the url: %s is available as at this time: %s" % (watch.url, time.asctime( time.localtime(timestamp) ))
    else:
        report = "[NOT-AVAILABLE] The site at the url: %s is not available as at this time: %s" % (watch.url, time.asctime( time.localtime(timestamp) ))
    
    # send the mail:
    send_email(watch.email, report)

    # record the check in the db:
    check = Check( watch_id=watch.id, report=report, timestamp=timestamp, mail_sent=True )
    db.session.add(check)
    db.session.commit()

    # create and send response
    response = {}
    response["check"] = check.to_json()
    response["status"] = "success"

    return json.dumps(response)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, body):
    app = current_app._get_current_object()
    msg = Message(app.config['MONITOR_BOT_REPORT_SUBJECT'], sender=app.config['MONITOR_BOT_MAIL_SENDER'], recipients=[to])
    msg.body = body
    
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
