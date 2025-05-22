from flask import Blueprint, request
from controllers import user as user_controller  # Evita conflito com variável 'user'
from http import HTTPStatus

app = Blueprint('auth', __name__, url_prefix='/auth')

GET = "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"

@app.route('/login', methods=[POST])
def _login():
    data = request.json

    if not data:
        return {"error": "Missing required fields"}, HTTPStatus.BAD_REQUEST

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Missing required fields"}, HTTPStatus.BAD_REQUEST

    found_user = user_controller._get_user_by_username(username)
    if not found_user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND

    if not found_user.check_password(password):
        return {"error": "Invalid password"}, HTTPStatus.UNAUTHORIZED

    return {
        "id": found_user.id,
        "username": found_user.username,
        "email": found_user.email,
    }, HTTPStatus.OK
