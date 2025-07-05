from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message
from sqlalchemy import inspect
from http import HTTPStatus
from werkzeug.security import generate_password_hash

from scr.controllers.models.models import User
from scr.db import db
from scr.token_utils import generate_confirmation_token
from app import mail

users = Blueprint('users', __name__, url_prefix='/users')

GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"

def log_audit(action: str, user_id: int, target_user_id: int = None):
    """
    Exemplo simples de função para criar logs de auditoria.
    Pode ser adaptada para gravar em tabela ou arquivo.
    """
    print(f"[{datetime.utcnow().isoformat()}] Usuário {user_id} realizou ação '{action}'"
          f"{' no usuário ' + str(target_user_id) if target_user_id else ''}")


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

    payload = {
        "username": data["username"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }
    token = generate_confirmation_token(payload)
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

    # Registrar auditoria: criação de usuário anônima (id=None)
    log_audit("create_user", user_id=None)

    return {"message": "Verifique seu e-mail para confirmar o cadastro."}, HTTPStatus.CREATED


def _list_users():
    query = db.select(User).where(User.deleted_at.is_(None))
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        for user in users
    ]


@users.route('/', methods=[GET, POST])
@jwt_required(optional=True)
def handler_user():
    if request.method == POST:
        return _create_user()
    else:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return {"error": "Autenticação requerida"}, HTTPStatus.UNAUTHORIZED

        current_user = User.query.get(current_user_id)
        if not current_user or not current_user.is_admin:
            return {"error": "Acesso negado"}, HTTPStatus.FORBIDDEN

        return {"users": _list_users()}


@users.route('/<int:user_id>', methods=[GET])
@jwt_required()
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user_id != user_id and not current_user.is_admin:
        return {"error": "Permissão negada"}, HTTPStatus.FORBIDDEN

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


@users.route('/<int:user_id>', methods=[PATCH])
@jwt_required()
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user_id != user_id and not current_user.is_admin:
        return {"error": "Permissão negada"}, HTTPStatus.FORBIDDEN

    data = request.json
    mapper = inspect(User)
    for column in mapper.columns:
        if column.name in data and (current_user.is_admin or column.name != "is_admin"):
            setattr(user, column.name, data[column.name])

    db.session.commit()

    log_audit("update_user", user_id=current_user_id, target_user_id=user_id)

    return {
        "id": user.id,
        "username": user.username,
    }, HTTPStatus.OK


@users.route('/<int:user_id>', methods=[DELETE])
@jwt_required()
def solicitar_exclusao(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "Usuário não encontrado"}, HTTPStatus.NOT_FOUND

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user_id != user_id and not current_user.is_admin:
        return {"error": "Permissão negada"}, HTTPStatus.FORBIDDEN

    user.deleted_at = datetime.utcnow()
    db.session.commit()

    log_audit("soft_delete_user", user_id=current_user_id, target_user_id=user_id)

    return {"message": "Solicitação de exclusão registrada."}, HTTPStatus.OK


