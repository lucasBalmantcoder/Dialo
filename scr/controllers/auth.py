from flask import Blueprint, request
from controllers import user
from http import HTTPStatus


app = Blueprint('auth', __name__, url_prefix='/auth')

GET =  "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"

@app.route('/', methods=[GET, POST])
def register_auth():
    if request.method == POST:
        return user.handler_user()
    else:
        return