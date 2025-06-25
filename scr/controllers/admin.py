from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from scr.controllers.models.models import AuditLog, User
from scr.db import db
from http import HTTPStatus
from scr.controllers.decorador.decorators import admin_required
from scr.controllers.utils.audit import log_audit  # import da função audit

admin = Blueprint('admin', __name__, url_prefix='/admin')

GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"


@admin.route('/login', methods=[POST])
def admin_login():
    data = request.json
    login_input = data.get("login")
    password = data.get("password")
    if not login_input or not password:
        return {"error": "Missing login or password"}, HTTPStatus.BAD_REQUEST

    user = User.query.filter(
        (User.username == login_input) | (User.email == login_input)
    ).first()

    if not user or not user.is_admin:
        return {"error": "Invalid admin credentials"}, HTTPStatus.UNAUTHORIZED

    from werkzeug.security import check_password_hash
    if not check_password_hash(user.password_with_hash, password):
        return {"error": "Invalid admin credentials"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))


    log_audit(user.id, "admin_login", f"Admin {user.username} logged in")

    return {"access_token": access_token}, HTTPStatus.OK


@admin.route('/users', methods=[GET])
@jwt_required()
@admin_required
def list_users():
    users = User.query.filter_by(deleted_at=None).all()
    result = [{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "is_admin": u.is_admin
    } for u in users]

    current_user_id = get_jwt_identity()
    log_audit(current_user_id, "list_users", f"Admin listed {len(users)} users")

    return jsonify(result), HTTPStatus.OK


@admin.route('/list_all_user_delete', methods=[GET])
@jwt_required()
@admin_required
def list_all_user_delete():
    current_user_id = get_jwt_identity()
    log_audit(current_user_id, "list_all_user_delete", "Admin listed all deleted users")

    return listar_excluidos(), HTTPStatus.OK


def listar_excluidos():
    query = db.select(User).where(User.deleted_at.is_not(None))
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None
        }
        for user in users
    ]


@admin.route('/<int:user_id>/hard-delete', methods=[DELETE])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    current_user_id = get_jwt_identity()
    log_audit(current_user_id, "hard_delete_user", f"Admin deleted user {user.username} (id: {user.id})")

    return "", HTTPStatus.NO_CONTENT


@admin.route('/audits', methods=[GET])
@jwt_required()
@admin_required
def list_audit_logs():
    """
    Rota para listar todos os registros de auditoria.
    Acesso restrito a administradores.
    """
    try:
        # Consulta todos os registros de auditoria no banco de dados
        audit_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

        # Formata os dados para a resposta JSON
        result = [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "timestamp": log.timestamp.isoformat(), # Converte para formato ISO 8601
                "details": log.details
            }
            for log in audit_logs
        ]

        # Registra a ação de auditoria (quem consultou os logs)
        current_user_id = get_jwt_identity()
        log_audit(current_user_id, "list_audit_logs", f"Admin listed {len(audit_logs)} audit logs")

        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        print(f"Erro ao listar auditorias: {e}")
        return jsonify({"error": "Erro interno ao processar a requisição"}), HTTPStatus.INTERNAL_SERVER_ERROR