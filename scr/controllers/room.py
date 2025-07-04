from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from scr.db import db
from scr.controllers.models.models import Room, User
from datetime import datetime

rooms = Blueprint('rooms', __name__, url_prefix='/rooms')

@rooms.route('/', methods=['POST'])
@jwt_required()
def create_room():
    data = request.json
    name = data.get("name")

    if not name:
        return {"error": "O nome da sala é obrigatório"}, HTTPStatus.BAD_REQUEST

    user_id = get_jwt_identity()
    new_room = Room(name=name, created_id=user_id)

    db.session.add(new_room)
    db.session.commit()

    return {
        "id": new_room.id,
        "name": new_room.name,
    }, HTTPStatus.CREATED

@rooms.route('/', methods=['GET'])
@jwt_required()
def list_rooms():
    rooms = Room.query.all()
    return [
        {
            "id": room.id,
            "name": room.name,
            "creator_id": room.created_id
        }
        for room in rooms
    ]

@rooms.route('/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    room = db.get_or_404(Room, room_id)
    return {
        "id": room.id,
        "name": room.name,
        "creator_id": room.created_id
    }

@rooms.route('/<int:room_id>', methods=['PATCH'])
@jwt_required()
def update_room(room_id):
    room = db.get_or_404(Room, room_id)
    user_id = get_jwt_identity()

    if room.created_id != user_id:
        return {"error": "Apenas o criador pode editar a sala."}, HTTPStatus.FORBIDDEN

    data = request.json
    if "name" in data:
        room.name = data["name"]
        db.session.commit()

    return {"message": "Sala atualizada com sucesso."}

@rooms.route('/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_room(room_id):
    room = db.get_or_404(Room, room_id)
    user_id = get_jwt_identity()

    if room.created_id != user_id:
        return {"error": "Apenas o criador pode excluir a sala."}, HTTPStatus.FORBIDDEN

    db.session.delete(room)
    db.session.commit()

    return {"message": "Sala excluída com sucesso."}
