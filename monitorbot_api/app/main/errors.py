from flask import render_template
from . import main


@main.app_errorhandler(404)
def resource_not_found(e):
    return 'IMPLEMENT-JSON-FORMATED-404-ERROR-RESPONSE-HERE', 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return 'IMPLEMENT-JSON-FORMATED-500-ERROR-RESPONSE-HERE', 500
