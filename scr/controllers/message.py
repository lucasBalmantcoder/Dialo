from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from scr.db import db
from scr.controllers.models.models import Message, Room, User, RoomUserAssociation # Importe RoomUserAssociation
import json

messages = Blueprint("messages", __name__, url_prefix="/messages")

@messages.route("/", methods=["POST"])
@jwt_required()
def enviar_mensagem():
    data = request.json
    user_id = get_jwt_identity()
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    room_id = data.get("room_id")
    encrypted_message_payload_str = data.get("message")

    if not room_id or not encrypted_message_payload_str:
        return {"error": "room_id e message são obrigatórios."}, HTTPStatus.BAD_REQUEST

    try:
        json.loads(encrypted_message_payload_str)
    except json.JSONDecodeError:
        return {"error": "O formato da mensagem criptografada é inválido (não é um JSON válido)."}, HTTPStatus.BAD_REQUEST

    room = db.get_or_404(Room, room_id)

    # Verifica se o usuário está na sala
    # user_ids_na_sala = [assoc.user_id for assoc in room.user_associations] # Pode ser ineficiente
    # Melhor verificar diretamente a associação:
    user_in_room = db.session.query(RoomUserAssociation).filter_by(user_id=user_id_int, room_id=room_id).first() # <-- USA O INTEIRO NO FILTRO

    if not user_in_room: # Se a associação não existe
        return {"error": "Você não pertence a esta sala."}, HTTPStatus.FORBIDDEN

    nova_msg = Message(
        room_id=room_id,
        user_id=user_id_int, # <-- USA O INTEIRO AQUI
        message=encrypted_message_payload_str
    )

    db.session.add(nova_msg)
    db.session.commit()

    return {"message": "Mensagem enviada com sucesso."}, HTTPStatus.CREATED


@messages.route("/<int:room_id>", methods=["GET"])
@jwt_required()
def listar_mensagens(room_id):
    user_id = get_jwt_identity()
    user_id_int = int(user_id) # <-- CONVERTE PARA INTEIRO AQUI

    room = db.get_or_404(Room, room_id)

    # Verifica se o usuário pertence à sala
    # user_ids_na_sala = [assoc.user_id for assoc in room.user_associations] # Pode ser ineficiente
    # Melhor verificar diretamente a associação:
    user_in_room = db.session.query(RoomUserAssociation).filter_by(user_id=user_id_int, room_id=room_id).first() # <-- USA O INTEIRO NO FILTRO

    if not user_in_room: # Se a associação não existe
        return {"error": "Você não pertence a esta sala."}, HTTPStatus.FORBIDDEN

    mensagens = Message.query.filter_by(room_id=room_id).order_by(Message.created).all()

    return [
        {
            "id": m.id,
            "autor": m.user_id,
            "mensagem": m.message,
            "criada_em": m.created.isoformat()
        } for m in mensagens
    ]
