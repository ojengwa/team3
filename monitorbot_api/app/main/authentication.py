from flask import g, request, json, jsonify
from ..models import User
from . import 
from .errors import unauthorized, forbidden


@main.route('/login/', methods=['POST'])
def login():

    # get credentials
    credentials = request.values.get('credentials')
    if not credentials:
         return bad_request("Invalid request format!")

    credentials = json.loads(credentials)
    if not ("email" in credentials and "password" in credentials):
        return bad_request("Invalid request format!")

    # check for a user with matching credentials
    user = User.query.filter_by(email=credentials.email).first()

    if user is not None and user.verify_password(credentials.password):
        # set the global current_user
        g.current_user = user
       
        # get auth_token for the user:
         auth_token = user.generate_auth_token(self, 3600*24)
        
        # create response
        response =  {}
        response.user: user.to_json()
        response.auth_token = auth_token

        return response

    else:
        return unauthorized("Invalid email or password!")


def auth_user(auth_token):
    g.current_user = User.verify_auth_token(auth_token)
    return g.current_user is not None





