from flask import Blueprint, request, url_for, current_app
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.security import check_password_hash, generate_password_hash
from scr.db import db
from scr.controllers.models.models import User
from flask_mail import Message
from app import mail

from scr.token_utils import confirm_token

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("login") or not data.get("password"):
        return {"error": "Missing login or password"}, HTTPStatus.BAD_REQUEST

    login_input = data["login"]
    password = data["password"]

    user = User.query.filter(
        (User.username == login_input) | (User.email == login_input)
    ).first()

    if not user:
        return {"error": "Invalid login or password"}, HTTPStatus.UNAUTHORIZED

    if user.is_blocked:
        return {"error": "Account is blocked. Please recover your account."}, HTTPStatus.FORBIDDEN

    if not check_password_hash(user.password_with_hash, password):
        user.login_attempts += 1
        if user.login_attempts >= 3:
            user.is_blocked = True
        db.session.commit()
        return {"error": "Invalid login or password"}, HTTPStatus.UNAUTHORIZED

    if not user.is_confirmed:
        return {"error": "Email not confirmed"}, HTTPStatus.UNAUTHORIZED

    # Reset attempts on successful login
    user.login_attempts = 0
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, HTTPStatus.OK

@auth.route('/confirm-email/<path:token>')
def confirm_email(token):
    try:
        data = confirm_token(token)
        if not data:
            return {"error": "Token inválido ou expirado"}, HTTPStatus.BAD_REQUEST

        # Verifica se o usuário já existe para evitar duplicidade
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "E-mail já confirmado."}, HTTPStatus.OK

        # Cria o usuário no banco só agora, confirmando o e-mail
        user = User(
            username=data["username"],
            email=data["email"],
            password_with_hash=data["password"],
            is_confirmed=True
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "E-mail confirmado e usuário criado com sucesso!"}, HTTPStatus.OK

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Erro interno: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

@auth.route('/teste-email')
def teste_email():
    msg = Message(
        subject="Testando envio de e-mail",
        recipients=["lucaspatrickr5@gmail.com"],
        body="Olá, my friend!!!!!!!!!!!!!!!!!!!!!!!"
    )
    mail.send(msg)
    return "E-mail enviado com sucesso!"

@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    if not email:
        return {"error": "Email is required"}, HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"message": "If this email is registered, you will receive instructions."}, HTTPStatus.OK

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt='password-reset-salt')
    reset_url = f"http://localhost:5173/reset-password/{token}"


    msg = Message(
        subject="Recuperação de senha",
        recipients=[email],
        body=f"Para resetar sua senha, acesse o link:\n{reset_url}\n\nEsse link expira em 1 hora."
    )
    mail.send(msg)

    return {"message": "Se o email estiver cadastrado, um link de recuperação foi enviado."}, HTTPStatus.OK


@auth.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json
    password = data.get("password")
    if not password:
        return {"error": "Password is required"}, HTTPStatus.BAD_REQUEST

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)
    except (SignatureExpired, BadSignature):
        return {"error": "Invalid or expired token"}, HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND

    user.password_with_hash = generate_password_hash(password)
    db.session.commit()

    return {"message": "Password has been reset successfully"}, HTTPStatus.OK



