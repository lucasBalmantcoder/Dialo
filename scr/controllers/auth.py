from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from scr.controllers.models.models import User

app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route('/login', methods=["POST"])
def _login():
    data = request.json

    if not data or not data.get("username") or not data.get("password"):
        return {"error": "Missing username or password"}, HTTPStatus.BAD_REQUEST

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_with_hash, password):
        return {"error": "Invalid username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=user.id)

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, HTTPStatus.OK
