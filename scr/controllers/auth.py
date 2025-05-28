from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from scr import db
from scr.controllers.models.models import User

#  Implementação da envio de e-mails
from flask_mail import Message
from app import mail

# IMportação do token
from scr.token_utils import generate_confirmation_token, confirm_token



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


@app.route('/teste-email')
def teste_email():
    msg = Message(
        subject="Testando envio de e-mail",
        recipients=["lucaspatrickr5@gmail.com"],
        body="Olá, my friend!!!!!!!!!!!!!!!!!!!!!!!"
    )
    mail.send(msg)
    return "E-mail enviado com sucesso!"



@app.route('/confirm-email/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return {"error": "Token inválido ou expirado"}, HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "Usuário não encontrado"}, HTTPStatus.NOT_FOUND

    user.is_confirmed = True
    db.session.commit()
    return {"message": "E-mail confirmado com sucesso!"}, HTTPStatus.OK
