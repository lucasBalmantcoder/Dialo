import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flask_mail import Message
from sqlalchemy import inspect

from scr.controllers.models.models import User
from scr.db import db
from http import HTTPStatus
from werkzeug.security import generate_password_hash

from scr.token_utils import generate_confirmation_token

from app import mail

# para salvar as informações temporiamente
from itsdangerous import URLSafeTimedSerializer
import json

serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY", "fallback_secreta"))

users = Blueprint('users', __name__, url_prefix='/users')

GET =  "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"


def _create_user():
    data = request.json
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return {"error": "Missing required fields"}, HTTPStatus.BAD_REQUEST

    errors = {}
    if User.query.filter_by(username=data["username"]).first():
        errors["username"] = "Username already exists"
    if User.query.filter_by(email=data["email"]).first():
        errors["email"] = "Email already exists"
    if errors:
        return {"errors": errors}, HTTPStatus.BAD_REQUEST

    # Cria o token com o payload completo (username, email, senha hash)
    payload = {
        "username": data["username"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }
    token = generate_confirmation_token(payload)

    # Mudar URL para frontend React
    confirm_url = f"http://localhost:5173/confirm-email/{token}"
    
    msg = Message(
        subject="Confirme seu e-mail",
        recipients=[data["email"]],
        body=f"Olá {data['username']}, clique no link para confirmar seu e-mail: {confirm_url}"
    )

    try:
        mail.send(msg)
    except Exception as e:
        return {"error": f"Erro ao enviar email: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {
        "message": "Verifique seu e-mail para confirmar o cadastro."
    }, HTTPStatus.CREATED

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()   
    
    return [ 
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.password_with_hash
        }
        for user in users
    ]

@users.route('/', methods=[GET, POST])
def handler_user():
    if request.method == POST:
        return _create_user()
    else:
        return {"users": _list_users()} 

@users.route('/<int:user_id>')
@jwt_required()
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "hashed_password": user.password_with_hash
    }
    
@users.route('/<int:user_id>', methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    user = db.get_or_404(User, user_id) 
    data = request.json

    mapper = inspect(User)
    for column in mapper.columns:
        if column.name in data:
            setattr(user, column.name, data[column.name])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }, HTTPStatus.OK

@users.route('/<int:user_id>', methods=["DELETE"])
# @jwt_required()
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
