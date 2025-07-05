from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from scr.db import db
from scr.controllers.models.models import Room, User, RoomUserAssociation # Importe RoomUserAssociation
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
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    new_room = Room(name=name, created_id=user_id_int) # <-- USA O INTEIRO
    db.session.add(new_room)
    db.session.commit()

    return {
        "id": new_room.id,
        "name": new_room.name,
    }, HTTPStatus.CREATED

@rooms.route('/', methods=['GET'])
@jwt_required()
def list_rooms():
    user_id = get_jwt_identity()
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    # Filtra as salas para mostrar apenas aquelas em que o usuário está associado
    user_rooms = db.session.query(Room).join(Room.user_associations).filter(RoomUserAssociation.user_id == user_id_int).all() # <-- USA O INTEIRO NO FILTRO

    return [
        {
            "id": room.id,
            "name": room.name,
            "creator_id": room.created_id,
            "users": [
                {
                    "id": assoc.user.id,
                    "username": assoc.user.username,
                    "email": assoc.user.email,
                    "public_key": assoc.user.public_key
                }
                for assoc in room.user_associations
            ]
        }
        for room in user_rooms
    ]


@rooms.route('/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    user_id = get_jwt_identity()
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    room = db.get_or_404(Room, room_id)

    # Verifica se o usuário pertence à sala antes de retornar os detalhes
    # user_in_room = any(assoc.user_id == user_id for assoc in room.user_associations)
    # A linha acima pode ser ineficiente para muitas associações. Melhor usar um filtro direto:
    user_in_room = db.session.query(RoomUserAssociation).filter_by(user_id=user_id_int, room_id=room_id).first() # <-- USA O INTEIRO NO FILTRO

    if not user_in_room:
        return {"error": "Você não pertence a esta sala."}, HTTPStatus.FORBIDDEN

    return {
        "id": room.id,
        "name": room.name,
        "creator_id": room.created_id,
        "users": [
            {
                "id": assoc.user.id,
                "username": assoc.user.username,
                "email": assoc.user.email,
                "public_key": assoc.user.public_key
            }
            for assoc in room.user_associations
        ]
    }

@rooms.route('/<int:room_id>', methods=['PATCH'])
@jwt_required()
def update_room(room_id):
    room = db.get_or_404(Room, room_id)
    user_id = get_jwt_identity()
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    if room.created_id != user_id_int: # <-- USA O INTEIRO
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
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    if room.created_id != user_id_int: # <-- USA O INTEIRO
        return {"error": "Apenas o criador pode excluir a sala."}, HTTPStatus.FORBIDDEN

    db.session.delete(room)
    db.session.commit()

    return {"message": "Sala excluída com sucesso."}
