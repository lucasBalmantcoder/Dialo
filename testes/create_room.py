import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scr.db import db
from scr.controllers.models.models import User, Room, RoomUserAssociation
from app import create_app  # Certifique-se de que o objeto `app` está importável de app.py

# IDs dos usuários que participarão da sala
user1_id = 2  # Altere conforme necessário
user2_id = 3 # Altere conforme necessário

# Nome da sala
room_name = "sala de conversa"

app = create_app()

with app.app_context():
    # Verificar existência dos usuários
    user1 = db.session.get(User, user1_id)
    user2 = db.session.get(User, user2_id)

    if not user1 or not user2:
        print("Erro: um ou ambos os usuários não existem.")
        exit(1)

    # Criar a sala
    new_room = Room(name=room_name, created_id=user1.id)
    db.session.add(new_room)
    db.session.commit()

    # Criar as associações
    assoc1 = RoomUserAssociation(user_id=user1.id, room_id=new_room.id)
    assoc2 = RoomUserAssociation(user_id=user2.id, room_id=new_room.id)

    db.session.add_all([assoc1, assoc2])
    db.session.commit()

    print(f"Sala '{new_room.name}' criada com ID {new_room.id}.")
    print(f"Usuários {user1.username} e {user2.username} adicionados à sala.")
