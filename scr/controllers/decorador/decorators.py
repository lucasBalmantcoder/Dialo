# scr/utils/decorators.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from http import HTTPStatus
from scr.controllers.models.models import User
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), HTTPStatus.FORBIDDEN
        return fn(*args, **kwargs)
    return wrapper
